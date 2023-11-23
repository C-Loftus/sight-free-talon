# edge-playback --text test
# run edge-playback with text as the first argument

# Check if there is at least one argument
if ($args.Length -ge 1) {
    # wrap all the args in a s 


    $singleArgument = '"' + ($args -join ' ') + '"' 

    # Execute the command
    try {
        edge-playback.exe --text $singleArgument
        Write-Output "Done."
        Write-Host "Done."
        #  write to stdo
    }
    catch {
        # write to stderr
        Write-Error $_
    }
}
else {
    Write-Host "Usage: ./RunCommand.ps1 <text-argument>"
    Write-Output "Usage: ./RunCommand.ps1 <text-argument>"
}