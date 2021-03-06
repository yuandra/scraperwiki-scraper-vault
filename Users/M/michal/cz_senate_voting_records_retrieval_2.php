<?php

require 'scraperwiki/simple_html_dom.php';

//corrections:
//scraperwiki::save_var('last_id',55626); //55150
/*scraperwiki::sqliteexecute("delete from info where id>55652");
scraperwiki::sqlitecommit();
die();*/

//get last id
//scraperwiki::save_var('last_id',0);
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_senate_voting_records_downloader_2", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));

    //common part
    $div = $dom->find("div[class=wysiwyg]",0);
        
    //info
    $h1 = $div->find('h1',0);
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
    preg_match('/([0-9]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
    preg_match('/([0-9]{2}).([0-9]{2}).([0-9]{4})/',$h1->innertext,$matches);
    $date = implode('-',array($matches[3],$matches[2],$matches[1]));

    $p = $div->find('p[class=openingText]',0);
    $p_ar = explode('<br />',$p->innertext);
    $name = $p_ar[0];
    if (isset($p_ar[1])) $detail = $p_ar[1]; else $detail = '';

    $span = $p->find('span',0);
    if (isset($span)) $proposal = $span->innertext; else $proposal='';

    if (strpos($div->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $passed = 'n';
    if (strpos($div->innertext,"NÁVRH BYL PŘIJAT") > 0) $passed = 'y';
    if (strpos($div->innertext,"ZMATEČNÉ HLASOVÁNÍ") > 0) $passed = '0';
    if (strpos($div->innertext,"NEVEŘEJNÁ ČÁST SCHŮZE") > 0) $passed = 'secret';

    preg_match('/PŘÍTOMNO=([0-9]{1,})/',$div->innertext,$matches);
    $present = $matches[1];
    preg_match('/JE TŘEBA=([0-9]{1,})/',$div->innertext,$matches);
    $needed = $matches[1];
    $data = array(
        'id' => $html['id'],
        'name' => $name,
        'date' => $date,
        'detail' => $detail,
        'proposal' => $proposal,
        'session' => $schuze,
        'division' => $hlasovani,
        'present' => $present,
        'needed' => $needed,
        'passed' => $passed,
    );
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
    $votes = array();
    $tables = $div->find('table');
    $h2s = $div->find('h2');
    array_shift($tables);
//print_r($tables);die();

    foreach ($tables as $key=>$table) {
      $tds = $table->find('td');
        foreach ($tds as $td) {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          $club = $h2s[$key]->innertext;
          $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $club,
          );
        }
    }
//print_r($votes);die();
    scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');

    /*$tds = $table->find('td');
    if (count($tds) > 0) {
      foreach ($tds as $td) {
//echo $td->outertext;
        $h3 = $td->find('h3',0);
        if ($h3 != '') {
          $party = $h3->innertext;
        } else {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          if ($mp != '') 
              $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $party,
              );
        }
      }
      scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');
    } */

  
    scraperwiki::save_var('last_id',$html['id']);
  }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

//corrections:
//scraperwiki::save_var('last_id',55626); //55150
/*scraperwiki::sqliteexecute("delete from info where id>55652");
scraperwiki::sqlitecommit();
die();*/

//get last id
//scraperwiki::save_var('last_id',0);
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_senate_voting_records_downloader_2", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));

    //common part
    $div = $dom->find("div[class=wysiwyg]",0);
        
    //info
    $h1 = $div->find('h1',0);
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
    preg_match('/([0-9]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
    preg_match('/([0-9]{2}).([0-9]{2}).([0-9]{4})/',$h1->innertext,$matches);
    $date = implode('-',array($matches[3],$matches[2],$matches[1]));

    $p = $div->find('p[class=openingText]',0);
    $p_ar = explode('<br />',$p->innertext);
    $name = $p_ar[0];
    if (isset($p_ar[1])) $detail = $p_ar[1]; else $detail = '';

    $span = $p->find('span',0);
    if (isset($span)) $proposal = $span->innertext; else $proposal='';

    if (strpos($div->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $passed = 'n';
    if (strpos($div->innertext,"NÁVRH BYL PŘIJAT") > 0) $passed = 'y';
    if (strpos($div->innertext,"ZMATEČNÉ HLASOVÁNÍ") > 0) $passed = '0';
    if (strpos($div->innertext,"NEVEŘEJNÁ ČÁST SCHŮZE") > 0) $passed = 'secret';

    preg_match('/PŘÍTOMNO=([0-9]{1,})/',$div->innertext,$matches);
    $present = $matches[1];
    preg_match('/JE TŘEBA=([0-9]{1,})/',$div->innertext,$matches);
    $needed = $matches[1];
    $data = array(
        'id' => $html['id'],
        'name' => $name,
        'date' => $date,
        'detail' => $detail,
        'proposal' => $proposal,
        'session' => $schuze,
        'division' => $hlasovani,
        'present' => $present,
        'needed' => $needed,
        'passed' => $passed,
    );
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
    $votes = array();
    $tables = $div->find('table');
    $h2s = $div->find('h2');
    array_shift($tables);
//print_r($tables);die();

    foreach ($tables as $key=>$table) {
      $tds = $table->find('td');
        foreach ($tds as $td) {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          $club = $h2s[$key]->innertext;
          $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $club,
          );
        }
    }
//print_r($votes);die();
    scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');

    /*$tds = $table->find('td');
    if (count($tds) > 0) {
      foreach ($tds as $td) {
//echo $td->outertext;
        $h3 = $td->find('h3',0);
        if ($h3 != '') {
          $party = $h3->innertext;
        } else {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          if ($mp != '') 
              $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $party,
              );
        }
      }
      scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');
    } */

  
    scraperwiki::save_var('last_id',$html['id']);
  }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

//corrections:
//scraperwiki::save_var('last_id',55626); //55150
/*scraperwiki::sqliteexecute("delete from info where id>55652");
scraperwiki::sqlitecommit();
die();*/

//get last id
//scraperwiki::save_var('last_id',0);
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_senate_voting_records_downloader_2", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));

    //common part
    $div = $dom->find("div[class=wysiwyg]",0);
        
    //info
    $h1 = $div->find('h1',0);
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
    preg_match('/([0-9]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
    preg_match('/([0-9]{2}).([0-9]{2}).([0-9]{4})/',$h1->innertext,$matches);
    $date = implode('-',array($matches[3],$matches[2],$matches[1]));

    $p = $div->find('p[class=openingText]',0);
    $p_ar = explode('<br />',$p->innertext);
    $name = $p_ar[0];
    if (isset($p_ar[1])) $detail = $p_ar[1]; else $detail = '';

    $span = $p->find('span',0);
    if (isset($span)) $proposal = $span->innertext; else $proposal='';

    if (strpos($div->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $passed = 'n';
    if (strpos($div->innertext,"NÁVRH BYL PŘIJAT") > 0) $passed = 'y';
    if (strpos($div->innertext,"ZMATEČNÉ HLASOVÁNÍ") > 0) $passed = '0';
    if (strpos($div->innertext,"NEVEŘEJNÁ ČÁST SCHŮZE") > 0) $passed = 'secret';

    preg_match('/PŘÍTOMNO=([0-9]{1,})/',$div->innertext,$matches);
    $present = $matches[1];
    preg_match('/JE TŘEBA=([0-9]{1,})/',$div->innertext,$matches);
    $needed = $matches[1];
    $data = array(
        'id' => $html['id'],
        'name' => $name,
        'date' => $date,
        'detail' => $detail,
        'proposal' => $proposal,
        'session' => $schuze,
        'division' => $hlasovani,
        'present' => $present,
        'needed' => $needed,
        'passed' => $passed,
    );
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
    $votes = array();
    $tables = $div->find('table');
    $h2s = $div->find('h2');
    array_shift($tables);
//print_r($tables);die();

    foreach ($tables as $key=>$table) {
      $tds = $table->find('td');
        foreach ($tds as $td) {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          $club = $h2s[$key]->innertext;
          $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $club,
          );
        }
    }
//print_r($votes);die();
    scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');

    /*$tds = $table->find('td');
    if (count($tds) > 0) {
      foreach ($tds as $td) {
//echo $td->outertext;
        $h3 = $td->find('h3',0);
        if ($h3 != '') {
          $party = $h3->innertext;
        } else {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          if ($mp != '') 
              $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $party,
              );
        }
      }
      scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');
    } */

  
    scraperwiki::save_var('last_id',$html['id']);
  }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

//corrections:
//scraperwiki::save_var('last_id',55626); //55150
/*scraperwiki::sqliteexecute("delete from info where id>55652");
scraperwiki::sqlitecommit();
die();*/

//get last id
//scraperwiki::save_var('last_id',0);
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;

//read the saved tables
scraperwiki::attach("cz_senate_voting_records_downloader_2", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
  foreach ($rows as $html) {
    //get dom
    $dom = new simple_html_dom();
    $html2 = scraperwiki::select("* from src.swdata where id={$html['id']}");
    $dom->load(str_replace("&nbsp;"," ",$html2[0]['html']));

    //common part
    $div = $dom->find("div[class=wysiwyg]",0);
        
    //info
    $h1 = $div->find('h1',0);
    preg_match('/([0-9]{1,}). schůze/',$h1->innertext,$matches);
    $schuze = $matches[1];
    preg_match('/([0-9]{1,}). hlasování/',$h1->innertext,$matches);
    $hlasovani = $matches[1];
    preg_match('/([0-9]{2}).([0-9]{2}).([0-9]{4})/',$h1->innertext,$matches);
    $date = implode('-',array($matches[3],$matches[2],$matches[1]));

    $p = $div->find('p[class=openingText]',0);
    $p_ar = explode('<br />',$p->innertext);
    $name = $p_ar[0];
    if (isset($p_ar[1])) $detail = $p_ar[1]; else $detail = '';

    $span = $p->find('span',0);
    if (isset($span)) $proposal = $span->innertext; else $proposal='';

    if (strpos($div->innertext,"NÁVRH BYL ZAMÍTNUT") > 0) $passed = 'n';
    if (strpos($div->innertext,"NÁVRH BYL PŘIJAT") > 0) $passed = 'y';
    if (strpos($div->innertext,"ZMATEČNÉ HLASOVÁNÍ") > 0) $passed = '0';
    if (strpos($div->innertext,"NEVEŘEJNÁ ČÁST SCHŮZE") > 0) $passed = 'secret';

    preg_match('/PŘÍTOMNO=([0-9]{1,})/',$div->innertext,$matches);
    $present = $matches[1];
    preg_match('/JE TŘEBA=([0-9]{1,})/',$div->innertext,$matches);
    $needed = $matches[1];
    $data = array(
        'id' => $html['id'],
        'name' => $name,
        'date' => $date,
        'detail' => $detail,
        'proposal' => $proposal,
        'session' => $schuze,
        'division' => $hlasovani,
        'present' => $present,
        'needed' => $needed,
        'passed' => $passed,
    );
//print_r($data);die();
    scraperwiki::save_sqlite(array('id'),$data,'info');

    //votes
    $votes = array();
    $tables = $div->find('table');
    $h2s = $div->find('h2');
    array_shift($tables);
//print_r($tables);die();

    foreach ($tables as $key=>$table) {
      $tds = $table->find('td');
        foreach ($tds as $td) {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          $club = $h2s[$key]->innertext;
          $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $club,
          );
        }
    }
//print_r($votes);die();
    scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');

    /*$tds = $table->find('td');
    if (count($tds) > 0) {
      foreach ($tds as $td) {
//echo $td->outertext;
        $h3 = $td->find('h3',0);
        if ($h3 != '') {
          $party = $h3->innertext;
        } else {
          $vote = substr($td->innertext,0,1);
          $mp = trim(substr($td->innertext,1));
          if ($mp != '') 
              $votes[] = array(
                'division_id' => $html['id'],
                'vote' => $vote,
                'mp' => $mp,
                'club' => $party,
              );
        }
      }
      scraperwiki::save_sqlite(array('division_id','mp'),$votes,'vote');
    } */

  
    scraperwiki::save_var('last_id',$html['id']);
  }
}

?>
