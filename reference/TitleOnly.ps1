#PULL IN VALUES FROM VANTAGE
param($arg1,$arg2,$arg3,$arg4,$arg5,$arg6,$arg7,$arg8)

$SourceDirectory = $arg1
$SourceVideoEDL = $arg2
$SourceAudioEDL = $arg3
$Outputfile = $arg4
#Not actually using this drop frame one yet
$DropFrame = $arg5
$FrameRate = "@" + $arg6
$NewblueCSV = $arg7
$ContentStartTC = $arg8

#splitting video edl into hash table variables by position.  This makes it easier to work with at all the steps below.
$videoarray = Get-Content $SourceDirectory\$SourceVideoEDL | select-object -skip 2
$fullvideoarray = @()
$tempvideoarray = @()
$videoarray += "------"

for ($a=0; $a -lt $videoarray.count; $a++) {
	#NewBlue files
	if ($videoarray[$a] -match ".nbtitle") {
	$Name = $videoarray[$a].substring(2)
	#Avid likes to make everything uppercase. This breaks Post Producer finding the file, so we set it to lowercase here.
	$Name = $Name.ToLower()
	$Start = $videoarray[$a-1].substring(53,11) -replace "(.*):(.*)", '$1;$2'
	$End = $videoarray[$a-1].substring(65,11) -replace "(.*):(.*)", '$1;$2'
	if ($videoarray[$a-1].substring(21,7) -ne "       " -and $videoarray[$a-1].substring(0,1) -ne "`*") {
	$Frames = [int]$videoarray[$a-1].substring(21,7) }
	else { 
	$Frames = 0 }
	$Dissolve = 0
	$Type = "Media"
	$tempvideoarray = new-object psobject
	$tempvideoarray | Add-member -membertype noteproperty -name "Name" -Value $Name
	$tempvideoarray | Add-member -membertype noteproperty -name "Start" -Value $Start
	$tempvideoarray | Add-member -membertype noteproperty -name "End" -Value $End
	$tempvideoarray | Add-member -membertype noteproperty -name "Transition_In" -Value $Frames
	$tempvideoarray | Add-member -membertype noteproperty -name "Transition_Out" -Value $Dissolve
	$tempvideoarray | Add-member -membertype noteproperty -name "Type" -Value $Type
	$fullvideoarray += $tempvideoarray
	}


#Assign Sources a unique number for the CML so there's no duplicates.
$sourcesarray = @()
$b=1
for ($a=0; $a -lt $fullvideoarray.count; $a++) {
	$Name = $fullvideoarray[$a].Name
	if (($fullvideoarray[$a].Type -eq "Media") -and ($sourcesarray -notcontains $Name)) {
	$tempsourcesarray = new-object psobject
	$tempsourcesarray | Add-member -membertype noteproperty -name "Name" -Value $Name
	$tempsourcesarray | Add-member -membertype noteproperty -name "Type" -Value "Video"
	$tempsourcesarray | Add-member -membertype noteproperty -name "Track" -Value $b
	$b++
	$sourcesarray += $tempsourcesarray
	}
	}


#Start creating the CML
Write-Output '<?xml version="1.0" encoding="utf-8"?>' | set-content $SourceDirectory\$outputfile
Write-Output '<Composition xmlns="Telestream.Soa.Facility.Playlist">' | add-content $SourceDirectory\$outputfile
Write-Output ('  <Source identifier="999999' + '"' +">") | add-content $SourceDirectory\$outputfile
Write-Output ('    <File location="{$#Original}' + '"' + ' />') | add-content $SourceDirectory\$outputfile
Write-Output ('    <Subtitle' + ' />') | add-content $SourceDirectory\$outputfile
Write-Output ('  </Source>') | add-content $SourceDirectory\$outputfile
for ($a=0; $a -lt $sourcesarray.count; $a++) {
	
    Write-Output ('  <Source identifier="' +$sourcesarray[$a].Track + '"' +">") | add-content $SourceDirectory\$outputfile
	Write-Output ('    <File location="{$$Source File Path}\' + $sourcesarray[$a].name + '"' + ' />') | add-content $SourceDirectory\$outputfile
	Write-Output ('  </Source>') | add-content $SourceDirectory\$outputfile
	
}
Write-Output '  <Sequence layer="1">' | add-content $SourceDirectory\$outputfile
Write-Output '   <Segment>' | add-content $SourceDirectory\$outputfile
Write-output ('    <Video source="999999"' + ' />') | add-content $SourceDirectory\$outputfile
Write-Output '   </Segment>' | add-content $SourceDirectory\$outputfile
Write-Output '  </Sequence>' | add-content $SourceDirectory\$outputfile

[int]$sequence = 2
#Add the video Sequences to CML
for ($a=0; $a -lt $fullvideoarray.count; $a++) {
	if ($fullvideoarray[$a].Type -eq "Image") {
	}
	Else {
	Write-Output ('  <Sequence layer="' + $sequence + '">') | add-content $SourceDirectory\$outputfile
	$source = $sourcesarray.GetEnumerator() | where-object {$_.Name -eq $fullvideoarray[$a].Name} | foreach-object {$_.Track}
	Write-Output '   <Segment>' | add-content $SourceDirectory\$outputfile
	Write-output ('    <Video source="' +$source + '"' + ' align="head" adjust="edge" offset="{' + $fullvideoarray[$a].Start + $FrameRate + '-' + $ContentStartTC + '}" filter="mute" >') | add-content $SourceDirectory\$outputfile
	Write-Output '       <Tail>' | add-content $SourceDirectory\$outputfile
	Write-output ('        <Edit mode="duration" time="{' + $fullvideoarray[$a].End + $FrameRate + '-' + $fullvideoarray[$a].Start + $FrameRate +'}"' + ' />') | add-content $SourceDirectory\$outputfile
	Write-Output '       </Tail>' | add-content $SourceDirectory\$outputfile
	Write-Output '     </Video>' | add-content $SourceDirectory\$outputfile
	Write-Output '   </Segment>' | add-content $SourceDirectory\$outputfile
	Write-Output '  </Sequence>' | add-content $SourceDirectory\$outputfile
	$sequence++
	}
}



Write-Output '</Composition>' | add-content $SourceDirectory\$outputfile

#Create the NewBlue CSV as needed.  It checks if it already exists or not before creating it.
$b = 1
if (!(test-path "$SourceDirectory\$Newbluecsv")) {
	for ($a=0; $a -lt $fullvideoarray.count; $a++) {
	if ($fullvideoarray[$a] | where {$_.Name -match "nbtitle"}) {
	Write-Output ($fullvideoarray[$a].Name + ',TFN') | add-content $SourceDirectory\$Newbluecsv
	#Write-Output ($fullvideoarray[$a].Name + ',{$$TEXT' + $b + '}') | add-content $SourceDirectory\$Newbluecsv
    Write-Output ($fullvideoarray[$a].Name + ',{$$TEXT1}') | add-content $SourceDirectory\$Newbluecsv
	$b++
	}
	}
}





	

