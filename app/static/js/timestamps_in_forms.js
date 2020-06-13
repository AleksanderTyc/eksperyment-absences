function zaladowaneBody() {
  var przychodzaca, domyslny, dzien_tyg;

//~ TODO:
//~ Potrzebne ustalanie wartosci domyslnych: https://momentjs.com/docs/#/manipulating/
//~ 1. 3 dni robocze do przodu.
//~ 1.1. Wez now: = moment()
//~ 1.2. Wez poczatek dnia .startOf( 'day' );
//~ 1.3. Oblicz dzien_tyg = isoWeekday
//~ 1.4. Dodaj 3 dni .add( 3, 'days' );
//~ 1.4. Jesli dzien_tyg +3 > 5 to dodaj jeszcze 2 dni .add( 2, 'days' );
//~ 2. od 8:00 do 12:00.
//~ 2.1. Do wyniku 1.5 dodaj odpowiednio 8 i 12 h. .add( 8 or 12, 'hours' );

  domyslny = moment().startOf( 'day' );
  dzien_tyg = domyslny.isoWeekday();
  if( dzien_tyg > 2 ) {
    domyslny.add( 5, 'days' );
  } else {
    domyslny.add( 3, 'days' );
  }
  
  przychodzaca = document.getElementById('ts_absence_start').value;
  if( przychodzaca == "None" ) {
    //~ przychodzaca = "2020-06-10 18:30:00";
    przychodzaca = domyslny.hour( 8 );
  }
  document.getElementById('ts_absence_start_vis').value = moment( moment.utc( przychodzaca ).format() ).format( "DD/MM/YYYY HH:mm" );
  console.log( przychodzaca )
  
  przychodzaca = document.getElementById('ts_absence_end').value;
  if( przychodzaca == "None" ) {
    //~ przychodzaca = "2020-06-10 19:30:00";
    przychodzaca = domyslny.hour( 12 );
  }
  document.getElementById('ts_absence_end_vis').value = moment( moment.utc( przychodzaca ).format() ).format( "DD/MM/YYYY HH:mm" );
  console.log( przychodzaca )
}

function date_start_vis_changed() {
//~ TODO:
//~ Potrzebna szczegolowa walidacja:
//~ 1. Czy daty sa w przyszlosci.
//~ 2. Czy daty sa wypelnione.
//~ 3. Czy daty sa poprawne. https://www.w3schools.com/js/js_validation.asp
  document.getElementById("ts_absence_start_vis").className = "form-control";
  document.getElementById("errMsgStart").innerHTML = null;
  document.getElementById("ts_absence_end_vis").className = "form-control";
  document.getElementById("errMsgEnd").innerHTML = null;
  if( !moment( document.getElementById('ts_absence_start_vis').value, "DD/MM/YYYY HH:mm" ).isValid() ) {
    document.getElementById("ts_absence_start_vis").className += " is-invalid";
    document.getElementById("errMsgStart").innerHTML = "Absence start date or time is invalid. Please correct.";
    document.getElementById("submit").setAttribute( "disabled", true )
  } else {
    document.getElementById('ts_absence_start').value = moment.utc( moment( document.getElementById('ts_absence_start_vis').value, "DD/MM/YYYY HH:mm" ).format() ).format( "YYYY-MM-DD HH:mm:ss" );
    document.getElementById('ts_absence_start_vis').value = moment( moment.utc( document.getElementById('ts_absence_start').value ).format() ).format( "DD/MM/YYYY HH:mm" );
    document.getElementById("submit").removeAttribute( "disabled" );
  }
  console.log( "X" +document.getElementById('ts_absence_start').value +"X X" +document.getElementById('ts_absence_end').value +"X" );
}

function date_end_vis_changed() {
//~ TODO:
//~ Potrzebna szczegolowa walidacja:
//~ 1. Czy daty sa w przyszlosci.
//~ 2. Czy daty sa wypelnione.
//~ 3. Czy daty sa poprawne. https://www.w3schools.com/js/js_validation.asp
  document.getElementById("ts_absence_start_vis").className = "form-control";
  document.getElementById("errMsgStart").innerHTML = null;
  document.getElementById("ts_absence_end_vis").className = "form-control";
  document.getElementById("errMsgEnd").innerHTML = null;
  if( !moment( document.getElementById('ts_absence_end_vis').value, "DD/MM/YYYY HH:mm" ).isValid() ) {
    document.getElementById("ts_absence_end_vis").className += " is-invalid";
    document.getElementById("errMsgEnd").innerHTML = "Absence end date or time is invalid. Please correct.";
    document.getElementById("submit").setAttribute( "disabled", true )
  } else {
    document.getElementById('ts_absence_end').value = moment.utc( moment( document.getElementById('ts_absence_end_vis').value, "DD/MM/YYYY HH:mm" ).format() ).format( "YYYY-MM-DD HH:mm:ss" );
    document.getElementById('ts_absence_end_vis').value = moment( moment.utc( document.getElementById('ts_absence_end').value ).format() ).format( "DD/MM/YYYY HH:mm" );
    document.getElementById("submit").removeAttribute( "disabled" );
  }
  console.log( "X" +document.getElementById('ts_absence_start').value +"X X" +document.getElementById('ts_absence_end').value +"X" );
}

function validateNewAbsence() {
  var m_start, m_end;
  m_start = moment.utc( document.getElementById('ts_absence_start').value );
  m_end = moment.utc( document.getElementById('ts_absence_end').value );
  if( !m_end.isAfter( m_start ) ) {
    document.getElementById("ts_absence_start_vis").className += " is-invalid";
    document.getElementById("errMsgStart").innerHTML = "End must be later than start. Please correct.";
    document.getElementById("ts_absence_end_vis").className += " is-invalid";
    document.getElementById("errMsgEnd").innerHTML = "End must be later than start. Please correct.";
    return false;
  } else {
    return true;
  }
}

//~~~~~~~~~~~~~~~~~~~ Smietnik ~~~~~~~~~~~~~~~~~~~~~~
function zaladowaneBodyOld() {
  console.log( "Load Base, URL: " +document.URL );
  var przychodzaca;
  var przychodzaca2;
  var przychodzaca3;
  przychodzaca = document.getElementById('ts_absence_start').value;
  //~ przychodzaca2 = przychodzaca.substr(0, przychodzaca.length -7 ).replace( " ", "T" ) +"+0:00"
  if( przychodzaca == "None" ) {
    przychodzaca = "2020-06-10 19:30:00";
  }
  //~ console.log( przychodzaca, przychodzaca2 );
  
  //~ document.getElementById('jsValueOfStart').innerHTML = "Jestem Agatka";
  //~ document.getElementById('jsValueOfStart').innerHTML = document.getElementById('ts_absence_start').value;
  document.getElementById('jsValueOfStart').innerHTML = przychodzaca;
  
  przychodzaca2 = moment.utc( przychodzaca ).format();
  document.getElementById('jsMomentValueOfStart').innerHTML = moment( przychodzaca2 ).format( "DD/MM/YYYY HH:mm" );
  przychodzaca3 = moment( przychodzaca2 ).format();
  console.log( "przychodzaca3: ", przychodzaca3 );
  
  document.getElementById('ts_absence_start_vis').value = moment( moment.utc( przychodzaca ).format() ).format( "DD/MM/YYYY HH:mm" );
}
