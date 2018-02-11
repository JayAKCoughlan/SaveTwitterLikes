Param
(
    [int] $saveLimit = 3,
    [Boolean] $ignoreSave = $false,
    [int] $tweetPull = 200,
    [String] $destination = '.\\images\\',
    [String] $pullFromID = "NON"
)

python .\Streaming_Twitter.py $saveLimit $ignoreSave $tweetPull $destination $pullFromID