include db open methods to app.py
--> done

include get_tasks route
--> done

include creation of ids in index.html to iterate the elements and replace html
--> done

https://stackoverflow.com/questions/1344030/how-can-i-use-jquery-load-to-replace-a-div-including-the-div
--> laden der DIVs geht ggf. viel einfacher

jQuery load adds the response INTO the element selected. jQuery's replaceWith REPLACES the selected element.

$.fn.loadWith = function(u){var c=$(this);$.get(u,function(d){c.replaceWith(d);});};
$("#test").loadWith("somelink.html");

--> done


Länger der Listen innerhalb einer Woche angleichen
--> done


Style für "done"
--> done

Deleted ausschließen
--> done


<ul> wird beim Nachladen der Inhalte ersetzt?
--> done --> loadWith2 nutzt nun die html Option um die Inhalte einzupflegen

Neuer Task als Form außerhalb des days.html templates
--> done

Event handler an createTask Form binden (über children hatte es für die Textfelder geklappt, aber span nicht)
--> Event handler hängt an den createTask Klassen (Eingaefelder) und abfeuern klappt.
--> es musste lediglich parent().parent().submit() sein um auch das DIV zu übergehen



Redirect soll auf letzte aktve seite gehen
--> done

Implement Toggle Task Handler & Route
- geht erstmal nict, weil Element noch nicht da ist, wenn script geladen wird
- in die Routine nach dem Laden der Inhalte eine Funktion aufrufen, die die Event Handler setzt
--> als event handler an body gebunden mit Verweis auf die Klasse...geht auch für dynamische Elemente



Done Date setzen
--> done

Favicon
--> done

Vertikale Ausrichtung der Tages Cards (align top)
--> done

Draggable Tasks
--> im DOM ja
muss noch in der DB abgebildet werden
positionen ermitteln
--> done


Delete Box
--> done

bei Klick auf Editbutton / Delete Button wird eine Hilfe angezeigt
--> done

Date field in schema.sql auf TEXT geändert, DB aber noch nicht neu erzeugt
--> done


!!! DA IST EIN BUG, der Tasks ohne Tagesbezug "undefined" in das date Feld schreibt und sie so unsichtbar macht!
--> done

erledigte Tasks sind jetzt auch draggable um Umsortieren zu vereinfachen
--> done


Modal für Editieren und Funktionen zum Update der DB
--> done


Hinweis auf Anlage der DB wenn noch nichts da ist
--> done


Anlegen neuer Task nicht mehr mit Reload / Standard Form SUbmit sondern jQuery


Nach Anlegen neuer Task wieder das Eingabefeld aktivieren


Backups erzeugen

initdb.py mit ein paar Demotasks mit AUfforderungen zum Ausprobieren generieren

Sprachen
https://phrase.com/blog/posts/flask-app-tutorial-i18n/

Auswertung
