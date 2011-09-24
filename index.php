<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <title>OpenBOE</title>
</head>

<body>
<?php 
    $ch = curl_init("http://www.boe.es/rss/canal.php?c=becas");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $data = curl_exec($ch);
    curl_close($ch);
    $doc = new SimpleXmlElement($data, LIBXML_NOCDATA);
    if(isset($doc->channel))
    {
        parseRSS($doc);
    }
    function parseRSS($xml)
    {
        echo "<strong>".$xml->channel->title."</strong>";
        $cnt = count($xml->channel->item);
        for($i=0; $i<$cnt; $i++)
        {
	        $url 	= $xml->channel->item[$i]->link;
	        $title 	= $xml->channel->item[$i]->title;
	        $desc = $xml->channel->item[$i]->description;
	        $guid = $xml->channel->item[$i]->guid;
            echo '<ul>';
	        echo '<li><a href="'.$url.'">'.$title.'</a>'.$desc.': <a href='.$guid.'>[PDF]</a></li><br />';
	        echo '</ul>';
        }
    }
?>
</body>
</html>
