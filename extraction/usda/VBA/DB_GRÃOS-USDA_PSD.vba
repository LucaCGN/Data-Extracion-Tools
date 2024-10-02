' API Key and Base URL
Const API_KEY As String = "697486e5-932d-46d3-804a-388452a19d70"
Const BASE_URL As String = "https://apps.fas.usda.gov/OpenData/api/psd/"

' Main Sub to Update All Data
Sub UpdateAllData()
    ' Step 1: Check if the table is up-to-date
    If Not ConfirmUpdate() Then Exit Sub
    
    ' Step 2: Update auxiliary tables
    UpdateRegions
    UpdateCountries
    UpdateCommodities
    UpdateUnitsOfMeasure
    UpdateCommodityAttributes
    
    ' Step 3: Fetch forecast data and update the final table
    UpdateFinalTable
    
    ' Step 4: Update the last update date in Home sheet
    UpdateLastUpdateDate
End Sub

' Function to confirm if update is necessary
Function ConfirmUpdate() As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Hist - USDA - PSD - Vertical")

    ' Find the most recent calendar year and month in the table
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "D").End(xlUp).row ' Assuming calendarYear is in column D

    Dim mostRecentYear As Long
    Dim mostRecentMonth As Long
    mostRecentYear = ws.Cells(lastRow, 4).value ' Column D for calendarYear
    mostRecentMonth = ws.Cells(lastRow, 5).value ' Column E for month

    ' Get the current year and month
    Dim currentYear As Long
    Dim currentMonth As Long
    currentYear = Year(Date)
    currentMonth = Month(Date)

    ' Check if the most recent entry matches the current year and month
    If mostRecentYear = currentYear And mostRecentMonth = currentMonth Then
        Dim userResponse As VbMsgBoxResult
        userResponse = MsgBox("The data appears to be up-to-date for the current month and year. Do you still want to proceed with the update?", vbYesNo + vbQuestion, "Confirm Update")
        
        If userResponse = vbNo Then
            ConfirmUpdate = False
            Exit Function
        End If
    End If

    ConfirmUpdate = True
End Function

' Function to Make HTTP GET Requests
Function GetAPIData(endpoint As String) As Object
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")

    Dim url As String
    url = BASE_URL & endpoint

    Debug.Print "Constructed URL: " & url ' Print the URL to the Immediate Window

    http.Open "GET", url, False
    http.setRequestHeader "Accept", "application/json"
    http.setRequestHeader "API_KEY", API_KEY
    http.send

    If http.Status = 200 Then
        Set GetAPIData = JsonConverter.ParseJson(http.responseText)
    Else
        MsgBox "Failed to fetch data from " & endpoint & ": " & http.Status & " " & http.StatusText
        Set GetAPIData = Nothing
    End If
End Function

' Update Regions
Sub UpdateRegions()
    Dim data As Object
    Set data = GetAPIData("regions")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("regionCode")
            arr(i, 2) = data(i)("regionName")
        Next i

        ' Sort the array by the second column (Region Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "O", "P")
    End If
End Sub

' Update Countries
Sub UpdateCountries()
    Dim data As Object
    Set data = GetAPIData("countries")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 4)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("countryCode")
            arr(i, 2) = data(i)("countryName")
            arr(i, 3) = data(i)("regionCode")
            arr(i, 4) = data(i)("gencCode")
        Next i

        ' Sort the array by the second column (Country Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "J", "M")
    End If
End Sub

' Update Commodities
Sub UpdateCommodities()
    Dim data As Object
    Set data = GetAPIData("commodities")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            ' Append a single quote to force Excel to treat the value as text
            arr(i, 1) = "'" & CStr(data(i)("commodityCode"))
            arr(i, 2) = data(i)("commodityName")
        Next i

        ' Sort the array by the second column (Commodity Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "A", "B")
    End If
End Sub

' Update Units of Measure
Sub UpdateUnitsOfMeasure()
    Dim data As Object
    Set data = GetAPIData("unitsOfMeasure")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("unitId")
            arr(i, 2) = data(i)("unitDescription")
        Next i

        ' Sort the array by the second column (Unit Description)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "G", "H")
    End If
End Sub

' Update Commodity Attributes
Sub UpdateCommodityAttributes()
    Dim data As Object
    Set data = GetAPIData("commodityAttributes")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("attributeId")
            arr(i, 2) = data(i)("attributeName")
        Next i

        ' Sort the array by the second column (Attribute Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "D", "E")
    End If
End Sub

' Main Sub to Update the Final Table
Sub UpdateFinalTable()
    Dim highlightedCommodities As Collection
    Dim highlightedAttributes As Scripting.Dictionary ' Use Scripting.Dictionary here
    
    ' Step 1: Get highlighted commodities and attributes
    Set highlightedCommodities = GetHighlightedCommodities()
    Set highlightedAttributes = GetHighlightedAttributes() ' This returns a Scripting.Dictionary
    
    ' Step 2: Prompt user for the first year and validate the input
    Dim startYear As Long
    Dim currentYear As Long
    Dim yearDifference As Long
    
    currentYear = Year(Date)
    
    ' Prompt user for the starting year
    startYear = Application.InputBox("Please enter the first year for the update (e.g., 2010):", "Start Year", 2010, Type:=1)
    
    ' Validate the input
    If startYear < 1960 Or startYear > currentYear Then
        MsgBox "Please enter a valid year between 1960 and " & currentYear, vbExclamation
        Exit Sub
    End If
    
    ' Check if the year range is more than 3 years
    yearDifference = currentYear - startYear
    If yearDifference > 3 Then
        Dim proceed As VbMsgBoxResult
        proceed = MsgBox("You have selected more than 3 years. This may result in slow performance and overhead in Excel. Do you want to proceed?", vbExclamation + vbYesNo, "Warning")
        If proceed = vbNo Then Exit Sub
    End If
    
    ' Step 3: Initialize a single-dimension array for storing the final data
    Dim finalData() As Variant
    Dim rowCount As Long
    rowCount = 0 ' Initial row count
    
    ' Loop through highlighted commodities and the selected range of years
    Dim commodityCode As String
    Dim item As Variant
    Dim marketYear As Long
    
    For Each item In highlightedCommodities
        commodityCode = item
        
        ' Loop through the years from the user-selected start year to the current year
        For marketYear = startYear To currentYear
            ' Fetch country-level and world-level data for this commodity and year
            Call FetchAndAppendData(commodityCode, marketYear, highlightedAttributes, finalData, rowCount)
        Next marketYear
    Next item
    
    ' Step 4: Write the final data array to the target sheet
    WriteDataToFinalTable finalData, rowCount
    
    ' Step 5: Update the date in the "Home" sheet after completion
    ThisWorkbook.Sheets("Home").Range("H3").value = Date
End Sub


' Fetch and append data for a specific commodity and year
Sub FetchAndAppendData(commodityCode As String, marketYear As Long, highlightedAttributes As Scripting.Dictionary, ByRef finalData() As Variant, ByRef rowCount As Long)
    Dim countryData As Object
    Dim worldData As Object
    
    ' Remove the leading quote from the commodity code for the API call
    commodityCode = Replace(commodityCode, "'", "")
    
    ' Fetch data for the commodity (country level and world level)
    Set countryData = GetAPIData("commodity/" & commodityCode & "/country/all/year/" & CStr(marketYear))
    Set worldData = GetAPIData("commodity/" & commodityCode & "/world/year/" & CStr(marketYear))
    
    ' Append country-level data to the finalData array
    If Not countryData Is Nothing Then
        Call AppendDataToFinalArray(countryData, highlightedAttributes, finalData, rowCount, False)
    End If
    
    ' Append world-level data to the finalData array
    If Not worldData Is Nothing Then
        Call AppendDataToFinalArray(worldData, highlightedAttributes, finalData, rowCount, True)
    End If
End Sub

' Function to append data to the final single-dimension array, joining with auxiliary data
Sub AppendDataToFinalArray(data As Object, highlightedAttributes As Scripting.Dictionary, ByRef finalData() As Variant, ByRef rowCount As Long, isWorldData As Boolean)
    Dim wsAux As Worksheet
    Set wsAux = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim i As Long
    Const numColumns As Long = 13 ' Number of columns
    
    For i = 1 To data.Count
        ' Only process if the attribute is highlighted
        If highlightedAttributes.Exists(data(i)("attributeId")) Then
            ' Increment the row count
            rowCount = rowCount + 1
            
            ' Resize the finalData array to hold the new row of data
            ReDim Preserve finalData(1 To rowCount * numColumns)
            
            ' Populate the finalData array (flattened structure)
            finalData((rowCount - 1) * numColumns + 1) = data(i)("commodityCode")
            
            ' Handle World Data
            If isWorldData Then
                finalData((rowCount - 1) * numColumns + 2) = "WO" ' Set country code as World (WO)
                finalData((rowCount - 1) * numColumns + 11) = "World" ' Set country name as World
                finalData((rowCount - 1) * numColumns + 12) = "Global" ' Set region name as Global
            Else
                ' Handle Regular Data
                finalData((rowCount - 1) * numColumns + 2) = data(i)("countryCode")
                finalData((rowCount - 1) * numColumns + 11) = GetAuxValue(data(i)("countryCode"), wsAux, "J", "K") ' Fetch country name
                finalData((rowCount - 1) * numColumns + 12) = GetRegionName(CStr(data(i)("countryCode")), wsAux) ' Fetch region name
            End If
            
            ' Common fields
            finalData((rowCount - 1) * numColumns + 3) = data(i)("marketYear")
            finalData((rowCount - 1) * numColumns + 4) = data(i)("calendarYear")
            finalData((rowCount - 1) * numColumns + 5) = data(i)("month")
            finalData((rowCount - 1) * numColumns + 6) = data(i)("attributeId")
            finalData((rowCount - 1) * numColumns + 7) = data(i)("unitId")
            finalData((rowCount - 1) * numColumns + 8) = GetAuxValue(data(i)("commodityCode"), wsAux, "A", "B") ' Commodity name
            finalData((rowCount - 1) * numColumns + 9) = GetAuxValue(data(i)("attributeId"), wsAux, "D", "E") ' Attribute name
            finalData((rowCount - 1) * numColumns + 10) = GetAuxValue(data(i)("unitId"), wsAux, "G", "H") ' Unit description
            finalData((rowCount - 1) * numColumns + 13) = data(i)("value")
        End If
    Next i
End Sub



' Write the final single-dimension array to the final table
Sub WriteDataToFinalTable(finalData() As Variant, rowCount As Long)
    Dim wsFinal As Worksheet
    Set wsFinal = ThisWorkbook.Sheets("Hist - USDA - PSD - Vertical")
    
    ' Only proceed if there is data to write
    If rowCount > 0 Then
        Dim i As Long, j As Long
        Dim numColumns As Long
        numColumns = 13 ' The fixed number of columns
        
        ' Write the data row by row
        For i = 1 To rowCount
            For j = 1 To numColumns
                wsFinal.Cells(i + 2, j).value = finalData((i - 1) * numColumns + j)
            Next j
        Next i
    End If
End Sub

' Function to get highlighted commodities from Tabelas AUX - USDA - PSD
Function GetHighlightedCommodities() As Collection
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim highlighted As New Collection
    Dim i As Long
    
    ' Loop through column A for highlighted commodities
    For i = 3 To ws.Cells(ws.Rows.Count, "A").End(xlUp).row
        If ws.Cells(i, 1).Interior.Color = RGB(255, 165, 0) Then ' Orange highlight
            highlighted.Add ws.Cells(i, 1).value
        End If
    Next i
    
    Set GetHighlightedCommodities = highlighted
End Function

' Function to get highlighted attributes from Tabelas AUX - USDA - PSD
Function GetHighlightedAttributes() As Scripting.Dictionary
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim highlighted As New Scripting.Dictionary
    Dim i As Long
    
    ' Loop through column D for highlighted attributes
    For i = 3 To ws.Cells(ws.Rows.Count, "D").End(xlUp).row
        If ws.Cells(i, 4).Interior.Color = RGB(255, 165, 0) Then ' Orange highlight
            highlighted.Add ws.Cells(i, 4).value, True
        End If
    Next i
    
    Set GetHighlightedAttributes = highlighted
End Function

' Function to get value from auxiliary table
Function GetAuxValue(key As Variant, ws As Worksheet, lookupCol As String, returnCol As String) As String
    Dim rng As Range
    Set rng = ws.Range(lookupCol & "3:" & lookupCol & ws.Cells(ws.Rows.Count, lookupCol).End(xlUp).row)
    
    Dim cell As Range
    Set cell = rng.Find(What:=CStr(key), LookIn:=xlValues, LookAt:=xlWhole) ' Convert key to string
    
    If Not cell Is Nothing Then
        GetAuxValue = cell.Offset(0, ws.Range(returnCol & "1").Column - ws.Range(lookupCol & "1").Column).value
    Else
        GetAuxValue = "" ' Handle the case where no match is found
    End If
End Function



' Function to retrieve region name using country code
Function GetRegionName(countryCode As String, ws As Worksheet) As String
    Dim countryRng As Range, regionRng As Range
    Dim countryCell As Range, regionCell As Range
    Dim regionCode As String
    
    ' Step 1: Find the country code in the countries table (columns J to L)
    Set countryRng = ws.Range("J3:J" & ws.Cells(ws.Rows.Count, "J").End(xlUp).row)
    Set countryCell = countryRng.Find(countryCode, LookIn:=xlValues, LookAt:=xlWhole)
    
    If Not countryCell Is Nothing Then
        ' Step 2: Retrieve the corresponding region code (column L)
        regionCode = countryCell.Offset(0, 2).value
        
        ' Step 3: Find the region code in the regions table (columns O to P)
        Set regionRng = ws.Range("O3:O" & ws.Cells(ws.Rows.Count, "O").End(xlUp).row)
        Set regionCell = regionRng.Find(regionCode, LookIn:=xlValues, LookAt:=xlWhole)
        
        If Not regionCell Is Nothing Then
            ' Step 4: Retrieve the corresponding region name (column P)
            GetRegionName = regionCell.Offset(0, 1).value
        Else
            GetRegionName = "" ' Region code not found
        End If
    Else
        GetRegionName = "" ' Country code not found
    End If
End Function

' Function to update the last update date in Home sheet
Sub UpdateLastUpdateDate()
    Dim wsHome As Worksheet
    Set wsHome = ThisWorkbook.Sheets("Home")
    
    ' Update cell H3 with the current date
    wsHome.Range("H3").value = Date
End Sub

' Function to sort a 2D array by a specified column
Sub SortArray(ByRef arr As Variant, ByVal sortColumn As Long)
    Dim i As Long, j As Long
    Dim temp As Variant

    For i = LBound(arr, 1) To UBound(arr, 1) - 1
        For j = i + 1 To UBound(arr, 1)
            If arr(i, sortColumn) > arr(j, sortColumn) Then
                ' Swap entire rows
                temp = arr(i, 1)
                arr(i, 1) = arr(j, 1)
                arr(j, 1) = temp
                
                temp = arr(i, 2)
                arr(i, 2) = arr(j, 2)
                arr(j, 2) = temp

                ' Continue swapping for additional columns if present
                If UBound(arr, 2) > 2 Then
                    Dim k As Long
                    For k = 3 To UBound(arr, 2)
                        temp = arr(i, k)
                        arr(i, k) = arr(j, k)
                        arr(j, k) = temp
                    Next k
                End If
            End If
        Next j
    Next i
End Sub

' Function to write array data to a worksheet while preserving formulas
Sub WriteArrayToSheet(ws As Worksheet, arr As Variant, startCol As String, endCol As String)
    Dim i As Long, j As Long
    Dim startRow As Long
    startRow = 3 ' Start writing data from row 3

    ' Loop through the array and write data to the worksheet, skipping cells with formulas
    For i = LBound(arr, 1) To UBound(arr, 1)
        For j = 1 To UBound(arr, 2)
            If Not ws.Cells(i + startRow - 1, j + ws.Range(startCol & "1").Column - 1).HasFormula Then
                ws.Cells(i + startRow - 1, j + ws.Range(startCol & "1").Column - 1).value = arr(i, j)
            End If
        Next j
    Next i
End Sub

