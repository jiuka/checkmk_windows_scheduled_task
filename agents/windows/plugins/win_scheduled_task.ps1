Write-Host '<<<win_scheduled_task:sep(9):encoding(cp437)>>>'
Get-ScheduledTask | Get-ScheduledTaskInfo | ForEach-Object {
    Write-Host "$($_.TaskPath)$($_.TaskName)`t$($_.LastTaskResult)`t$($_.LastRunTime)`t$($_.NextRunTime)"
}
