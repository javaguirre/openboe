<?php

    function readFeed($feed)
    {
        $ch = curl_init($feed);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $data = curl_exec($ch);
        curl_close($ch);
        $doc = new SimpleXmlElement($data, LIBXML_NOCDATA);
        if(isset($doc->channel))
        {
            $result = parseRSS($doc);
        }

        return $result;
    }

    function parseRSS($xml)
    {
//         echo "<strong>".$xml->channel->title."</strong>";
        $cnt = count($xml->channel->item);
        $result = array();
        
        for($i=0; $i<$cnt; $i++)
        {
	        $result[$i] = array('url'       => $xml->channel->item[$i]->link, 
                                'title'     => $xml->channel->item[$i]->title,
                                'desc'      => $xml->channel->item[$i]->description,
                                'guid'      => $xml->channel->item[$i]->guid
            );
        }

        return $result;
    }

    function searchItem($text)
    {   //TODO feed dont has to rebuild every time
        $feedValues = readFeed('http://www.boe.es/rss/canal.php?c=becas');
        foreach($feedValues as $key=>$feed)
        {
            if(!stristr($feed['title'], $text))
            {
                unset($feedValues[$key]);
            }
        }

        return $feedValues;
    }
    
?>