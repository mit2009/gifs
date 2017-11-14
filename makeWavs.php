<html>
<head>
        <title>Crowdpattern GIF generator</title>
        <link rel="stylesheet" href="../parent.css">
        <link rel="stylesheet" href="../page.css">
        <link href="../lightbox/css/lightbox.css" rel="stylesheet" />
        <link rel="icon" type="image/png" href="../favicon.png" />
        <link href='http://fonts.googleapis.com/css?family=Roboto:400,700,500' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
</head>

<body>
<h1>Coordinate crowds using GIFs!</h1>

<?php
set_time_limit(300);
//echo "working<br><br>";

$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is actual image or fake image
if(isset($_POST["submit"])) {
	$check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
	if($check !== false) {
		echo "File is an image - " . $check["mime"] . ".";
		$UploadOk = 1;
	} else {
		echo "File is not an image.<br><br>";
		$uploadOk = 0;
	}
}
// Check file size
if ($_FILES["fileToUpload"]["size"] > 5000000) {
	echo "Sorry, your file is too large.<br><br>";
	$uploadOk = 0;
}
// Allow certain file formats
if($imageFileType != "gif") {
	echo "Sorry, only GIF files are allowed.<br><br>";
	$uploadOk = 0;
}
// Check if $uploadOk is set to 0 by some reason
if ($uploadOk == 0) {
	echo "Sorry, your file was not uploaded.<br><br>";
} else {
	if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
		echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded succesfully.<br><br>";
	} else {
		echo "Sorry, there was an error uploading your file.";
	}
}

$fn = escapeshellarg("{$_FILES["fileToUpload"]["name"]}"); //filename
$timeStep = escapeshellarg("{$_POST["time"]}"); //timestep
$delay = escapeshellarg("{$_POST["delay"]}"); //delay

//echo exec("whoami") . "<br>";

$result = passthru('python gifRead.py '.$fn.' '.$timeStep.' '.$delay);
echo $result;
//echo 'done';

?>
<br><br><h2>Access your files <a href="/gifs/wavs">here</a>.</h2>
<p>Web interface &amp script by Landon Carter, concept by Victor Hung.</p>
<p>Questions? Bugs? Requests? <a href="mailto:crowdGIF-admin@mit.edu">Email us</a>.</p>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-57039341-1', 'auto');
  ga('send', 'pageview');

</script>
</body>


</html>

