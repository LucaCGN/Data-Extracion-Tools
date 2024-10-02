Sub FetchAndLoadWASDEDataForMissingDates()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Hist - USDA - WASDE - Vertical")

    ' Turn off screen updating and automatic calculation to improve performance
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo CleanUp

    ' Find the most recent date in the ReportDate column (Column B)
    Dim lastRow As Long
    Dim lastReportDate As Date
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).row
    lastReportDate = ws.Cells(lastRow, "B").value ' Assuming the date is in Column B

    ' Get the current date
    Dim currentDate As Date
    currentDate = Date

    ' If the most recent date matches the current month and year, show a message and exit
    If Format(lastReportDate, "mm/yyyy") = Format(currentDate, "mm/yyyy") Then
        MsgBox "Current data is up to date.", vbInformation
        GoTo CleanUp
    End If

    ' Generate URLs for the CSV files between the most recent report date and the current date
    Dim csvUrls As Collection
    Set csvUrls = GenerateCSVUrls(lastReportDate, currentDate)

    ' Prompt the user with the list of URLs that will be fetched
    Dim url As Variant
    Dim urlList As String
    For Each url In csvUrls
        urlList = urlList & url & vbCrLf
    Next url

    Dim userResponse As VbMsgBoxResult
    userResponse = MsgBox("The following reports will be fetched:" & vbCrLf & urlList & vbCrLf & "Do you want to proceed?", vbYesNo + vbQuestion, "Confirm Report Fetch")

    If userResponse = vbNo Then GoTo CleanUp

    ' List of selected reports
    Dim selectedReports As Variant
    selectedReports = Array("U.S. Wheat Supply and Use", "World Soybean Oil Supply and Use", "World Wheat Supply and Use", _
                            "Mexico Sugar Supply and Use and High Fructose Corn Syrup Consumption", "U.S. Cotton Supply and Use", _
                            "U.S. Wheat by Class: Supply and Use", "U.S. Soybeans and Products Supply and Use (Domestic Measure)", _
                            "World Cotton Supply and Use", "World Corn Supply and Use", "U.S. Feed Grain and Corn Supply and Use", _
                            "World and U.S. Supply and Use for Oilseeds", "World Soybean Supply and Use", "World and U.S. Supply and Use for Cotton", _
                            "World Soybean Meal Supply and Use")

    ' Loop through each CSV URL and process data
    For Each url In csvUrls
        If Not ProcessCSVData(url, ws, selectedReports) Then
            MsgBox "Report not released for URL: " & url, vbExclamation
        End If
    Next url

    MsgBox "Data loaded successfully.", vbInformation

CleanUp:
    ' Restore screen updating and calculation
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic

    ' Error handling
    If Err.Number <> 0 Then
        MsgBox "An error occurred: " & Err.Description, vbExclamation
    End If
End Sub

Function GenerateCSVUrls(startDate As Date, endDate As Date) As Collection
    Dim csvUrls As New Collection
    Dim currentDate As Date
    Dim yearStr As String, monthStr As String
    Dim baseUrl As String

    baseUrl = "https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-"

    ' Start generating URLs from the month after the most recent date in the table
    currentDate = DateAdd("m", 1, startDate)
    
    ' Loop through each month and year in the specified date range
    Do While currentDate <= endDate
        yearStr = Format(currentDate, "yyyy")
        monthStr = Format(currentDate, "mm")
        
        ' Generate the URL for the current month and year
        csvUrls.Add baseUrl & yearStr & "-" & monthStr & ".csv"
        
        ' Move to the next month
        currentDate = DateAdd("m", 1, currentDate)
    Loop

    Set GenerateCSVUrls = csvUrls
End Function



Function ProcessCSVData(ByVal csvURL As String, ws As Worksheet, selectedReports As Variant) As Boolean
    On Error GoTo CleanUp

    ' Download CSV data
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", csvURL, False
    http.send

    If http.Status <> 200 Then
        ' Skip if the CSV is not found or cannot be downloaded
        ProcessCSVData = False
        Exit Function
    End If

    ' Split CSV content into lines
    Dim csvContent As String
    csvContent = http.responseText
    Dim csvLines() As String
    csvLines = Split(csvContent, vbCrLf)

    ' Variables to process CSV data
    Dim i As Long
    Dim dataFields() As String
    Dim rowCount As Long
    Dim dataArray As Variant
    Dim dataIndex As Long

    ' Prepare array to store data (optimize for bulk writing)
    ReDim dataArray(1 To UBound(csvLines), 1 To 16)
    dataIndex = 1
    rowCount = ws.Cells(ws.Rows.Count, "A").End(xlUp).row + 1 ' Start from the next available row

    ' Process each line of the CSV (skipping the header)
    For i = 1 To UBound(csvLines) ' Skip the first line which is the header
        If Len(Trim(csvLines(i))) > 0 Then
            dataFields = ParseCSVLine(csvLines(i))
            
            ' Ensure that the line has the expected number of fields (16 in this case)
            If UBound(dataFields) = 15 Then
                ' Check if the report title is in the selected reports list
                If IsInArray(Trim(dataFields(2)), selectedReports) Then
                    ' Store the data in the array
                    dataArray(dataIndex, 1) = dataFields(0)
                    dataArray(dataIndex, 2) = dataFields(1)
                    dataArray(dataIndex, 3) = dataFields(2)
                    dataArray(dataIndex, 4) = dataFields(3)
                    dataArray(dataIndex, 5) = dataFields(4)
                    dataArray(dataIndex, 6) = dataFields(5)
                    dataArray(dataIndex, 7) = dataFields(6)
                    dataArray(dataIndex, 8) = dataFields(7)
                    dataArray(dataIndex, 9) = dataFields(8)
                    dataArray(dataIndex, 10) = dataFields(9)
                    dataArray(dataIndex, 11) = dataFields(10)
                    dataArray(dataIndex, 12) = dataFields(11)
                    dataArray(dataIndex, 13) = dataFields(12)
                    dataArray(dataIndex, 14) = dataFields(13)
                    dataArray(dataIndex, 15) = dataFields(14)
                    dataArray(dataIndex, 16) = dataFields(15)
                    dataIndex = dataIndex + 1
                End If
            End If
        End If
    Next i

    ' Write the entire array to the worksheet in one go
    If dataIndex > 1 Then
        ws.Range("A" & rowCount).Resize(dataIndex - 1, 16).value = dataArray
    End If

    ProcessCSVData = True

CleanUp:
    ' Clean up
    Set http = Nothing

    If Err.Number <> 0 Then
        MsgBox "An error occurred: " & Err.Description, vbExclamation
    End If
End Function

Function ParseCSVLine(ByVal csvLine As String) As Variant
    Dim fields As Collection
    Set fields = New Collection
    Dim currentField As String
    Dim inQuotes As Boolean
    Dim i As Long

    inQuotes = False
    currentField = ""

    For i = 1 To Len(csvLine)
        Dim currentChar As String
        currentChar = Mid(csvLine, i, 1)

        If currentChar = """" Then
            ' Toggle the inQuotes flag when encountering a quote
            inQuotes = Not inQuotes
        ElseIf currentChar = "," And Not inQuotes Then
            ' If not inside quotes, treat the comma as a field delimiter
            fields.Add currentField
            currentField = ""
        Else
            ' Append character to the current field
            currentField = currentField & currentChar
        End If
    Next i

    ' Add the last field
    fields.Add currentField

    ' Convert collection to array
    Dim arr() As String
    ReDim arr(0 To fields.Count - 1)
    For i = 1 To fields.Count
        arr(i - 1) = fields(i)
    Next i

    ParseCSVLine = arr
End Function

Function IsInArray(value As String, arr As Variant) As Boolean
    Dim i As Long
    For i = LBound(arr) To UBound(arr)
        If arr(i) = value Then
            IsInArray = True
            Exit Function
        End If
    Next i
    IsInArray = False
End Function


