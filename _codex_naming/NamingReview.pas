Procedure ProbeNamingAPI;
Var
    Log : TStringList;
    Doc : ISch_Document;
Begin
    Log := TStringList.Create;
    Try
        Log.Add('SCRIPT_STARTED');
        Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\probe.txt');
        Doc := SchServer.GetCurrentSchDocument;
        If Doc <> Nil Then Log.Add('CURRENT_SCH=' + Doc.DocumentName);
        Log.Add('SCRIPT_FINISHED');
        Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\probe.txt');
    Finally
        Log.Free;
    End;
End;

Procedure ExportNamingTopology;
Var
    WS : IWorkspace;
    Project, Candidate : IProject;
    Doc : IDocument;
    Comp : IPart;
    Pin : IPin;
    Net : INet;
    NetItem : INetItem;
    Violation : IViolation;
    Log, Status, StageList, Labels, Violations : TStringList;
    I, J, K, P : Integer;
    Stage, Compiled : String;
Begin
    Log := TStringList.Create;
    Status := TStringList.Create;
    StageList := TStringList.Create;
    Labels := TStringList.Create;
    Violations := TStringList.Create;
    Try
        StageList.LoadFromFile('D:\Route-ECU-Hardware\_codex_naming\stage.txt');
        Stage := StageList[0];
        WS := GetWorkspace;
        Project := Nil;
        For P := 0 To WS.DM_ProjectCount - 1 Do
        Begin
            Candidate := WS.DM_Projects(P);
            If SameText(Candidate.DM_ProjectFullPath, 'D:\Route-ECU-Hardware\ECTU.PrjPcb') Then Project := Candidate;
        End;
        If Project = Nil Then
        Begin
            Status.Add('PROJECT_NOT_FOUND');
            Status.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\topology_' + Stage + '_status.txt');
            Exit;
        End;
        If Project.DM_Compile Then Compiled := 'TRUE' Else Compiled := 'FALSE';
        Status.Add('COMPILE_RETURN=' + Compiled);
        Status.Add('PHYSICAL_DOCS=' + IntToStr(Project.DM_PhysicalDocumentCount));
        Log.Add('FILE'#9'COMPONENT'#9'PIN'#9'PIN_NAME'#9'NET');
        Labels.Add('FILE'#9'UID'#9'ID'#9'NET');
        For I := 0 To Project.DM_PhysicalDocumentCount - 1 Do
        Begin
            Doc := Project.DM_PhysicalDocuments(I);
            For J := 0 To Doc.DM_NetCount - 1 Do
            Begin
                Net := Doc.DM_Nets(J);
                For K := 0 To Net.DM_PowerObjectCount - 1 Do
                Begin
                    NetItem := Net.DM_PowerObjects(K);
                    Labels.Add(ExtractFileName(Doc.DM_FullPath) + #9 + NetItem.DM_FullUniqueId + #9 + NetItem.DM_Id + #9 + NetItem.DM_FlattenedNetName);
                End;
            End;
            For J := 0 To Doc.DM_ComponentCount - 1 Do
            Begin
                Comp := Doc.DM_Components(J);
                For K := 0 To Comp.DM_PinCount - 1 Do
                Begin
                    Pin := Comp.DM_Pins(K);
                    Log.Add(ExtractFileName(Doc.DM_FullPath) + #9 + Comp.DM_FullLogicalDesignator + #9 + Pin.DM_PinNumber + #9 + Pin.DM_PinName + #9 + Pin.DM_FlattenedNetName);
                End;
            End;
        End;
        Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\topology_' + Stage + '.tsv');
        Labels.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\compiled_labels_' + Stage + '.tsv');
        For I := 0 To Project.DM_ViolationCount - 1 Do
        Begin
            Violation := Project.DM_Violations(I);
            Violations.Add(IntToStr(Ord(Violation.DM_ErrorLevel)) + #9 + Violation.DM_DescriptorString + #9 + Violation.DM_DetailString);
        End;
        Violations.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\violations_' + Stage + '.tsv');
        Status.Add('VIOLATIONS=' + IntToStr(Project.DM_ViolationCount));
        Status.Add('EXPORT_FINISHED');
        Status.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\topology_' + Stage + '_status.txt');
    Finally
        Log.Free;
        Status.Free;
        StageList.Free;
        Labels.Free;
        Violations.Free;
    End;
End;

Procedure InventoryPCB;
Var
    Board : IPCB_Board;
    ServerDoc : IServerDocument;
    It : IPCB_BoardIterator;
    Net : IPCB_Net;
    Log : TStringList;
Begin
    Log := TStringList.Create;
    Try
        ServerDoc := Client.OpenDocument('PCB', 'D:\Route-ECU-Hardware\ECTU_PCB.PcbDoc');
        Board := PCBServer.GetPCBBoardByPath('D:\Route-ECU-Hardware\ECTU_PCB.PcbDoc');
        If ServerDoc.Modified Then Log.Add('DIRTY_PCB');
        It := Board.BoardIterator_Create;
        It.AddFilter_ObjectSet(MkSet(eNetObject));
        It.AddFilter_LayerSet(AllLayers);
        It.AddFilter_Method(eProcessAll);
        Try
            Net := It.FirstPCBObject;
            While Net <> Nil Do
            Begin
                Log.Add(Net.Name);
                Net := It.NextPCBObject;
            End;
        Finally
            Board.BoardIterator_Destroy(It);
        End;
        Log.Add('PCB_INVENTORY_FINISHED');
        Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\pcb_names.txt');
    Finally
        Log.Free;
    End;
End;

Procedure InventoryNaming;
Var
    Files, Log : TStringList;
    Doc : ISch_Document;
    ServerDoc : IServerDocument;
    Iterator : ISch_Iterator;
    Obj : ISch_GraphicalObject;
    I, Count : Integer;
Begin
    Files := TStringList.Create;
    Log := TStringList.Create;
    Try
        Files.LoadFromFile('D:\Route-ECU-Hardware\_codex_naming\files.txt');
        Log.Add('FILE'#9'TYPE'#9'NAME'#9'X'#9'Y');
        For I := 0 To Files.Count - 1 Do
        Begin
            ServerDoc := Client.OpenDocument('SCH', Files[I]);
            Doc := SchServer.GetSchDocumentByPath(Files[I]);
            If Doc = Nil Then
            Begin
                Log.Add('ERROR_DOCUMENT_NOT_LOADED'#9 + Files[I]);
                Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\inventory.tsv');
                Exit;
            End;
            If ServerDoc.Modified Then Log.Add('DIRTY'#9 + Files[I]);
            Iterator := Doc.SchIterator_Create;
            Iterator.AddFilter_ObjectSet(MkSet(ePowerObject));
            Try
                Obj := Iterator.FirstSchObject;
                While Obj <> Nil Do
                Begin
                    Log.Add(ExtractFileName(Files[I]) + #9 + IntToStr(Obj.ObjectId) + #9 + Obj.Text + #9 + IntToStr(Obj.Location.X) + #9 + IntToStr(Obj.Location.Y));
                    Obj := Iterator.NextSchObject;
                End;
            Finally
                Doc.SchIterator_Destroy(Iterator);
            End;
        End;
        Log.Add('INVENTORY_FINISHED');
        Log.SaveToFile('D:\Route-ECU-Hardware\_codex_naming\inventory.tsv');
    Finally
        Files.Free;
        Log.Free;
    End;
End;
