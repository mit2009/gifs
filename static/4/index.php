<html>
<head>
        <title>Crowdpattern GIF generator</title>
        <link rel="stylesheet" href="../../../parent.css">
        <link rel="stylesheet" href="../../../page.css">
	<link rel="stylesheet" href="table.css">
	<link rel="stylesheet" href="button.css">
	<link rel="stylesheet" href="button2.css">
        <link rel="icon" type="image/png" href="../../../favicon.png" />
        <link href='http://fonts.googleapis.com/css?family=Roboto:400,700,500' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
</head>

<body>
<h1>Click on your place in the crowd below.</h1>
<h2>(FRONT)</h2>
<table>
<?php
$myfile = fopen("size.txt","r") or die("Unable to determine size.");
$xDim = intval(fgets($myfile));
$yDim = intval(fgets($myfile));
fclose($myfile);

for ($i = 1; $i <= $xDim; $i++)
{
	echo "<tr>";
	for ($j = 1; $j <= $yDim; $j++)
	{
		echo "<td><a class=\"button\" href={$j}_{$i}.wav></a></td>";
	}
	echo "</tr>";
}

?>
</table>
<br><div align="center"><a class="button2" href="../..">Done!</a></div>
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

