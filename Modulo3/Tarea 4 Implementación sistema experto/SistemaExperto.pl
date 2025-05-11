:- dynamic realizando_tramite/1, tramite/1, presento_admision/1, 
   lista_aceptados/1, cuota/1, cursos/1, lista_aspirantes/1, preinscrito/1,
   entrego_documentacion/1, aceptacion_docu/1, inscrito/1, creditos/1, grupo/1, folio/1, 
   carta/1, reportes/1, evaluacion/1, informe/1.

:- discontiguous ver_grupo/0, ver_induccion/0, ver_registro_folio/0, ver_carta/0, ver_entrega_reportes/0,
    ver_evaluacion/0, ver_terminacion/0, ver_informe_final/0, ver_carta_liberacion/0.

realizando_tramite(0).
tramite(0).
presento_admision(0).
lista_aceptados(0).
cuota(0).
cursos(0).
lista_aspirantes(0).
preinscrito(0).
entrego_documentacion(0).
aceptacion_docu(0).
inscrito(0).
creditos(0).
grupo(0).
folio(0).
carta(0).
reportes(0).
evaluacion(0).

preguntar_si_tramite:-
    write("¿Estás realizando algún trámite?"),nl,
    write( "1. si, 2. no"),
    read(Tramite),
    retractall(realizando_tramite(_)), assertz(realizando_tramite(Tramite)),
    ((Tramite<1; Tramite>2),nl, write("Por favor, usa solo 1 para si y 2 para no"),
        nl, preguntar_si_tramite); true.

menu_tramite :-
    write("¿Qué trámite estás haciendo?"), nl,
    write("1. Preinscripción"), nl,
    write("2. Inscripción"), nl,
    write("3. Reinscripción"), nl,
    write("4. Servicio social"), nl,
    write("5. Titulación"), nl,
    read(Tramite),
    (Tramite >= 1, Tramite =< 5 ->
        retractall(tramite(_)), assertz(tramite(Tramite));
        write("Por favor selecciona una opción válida del 1 al 5."), nl,
        menu_tramite).

revisar_que_rollo_con_el_tramite:-
    (tramite(1), ver_preinscripcion);
    (tramite(2), ver_inscripcion);
    (tramite(3), ver_reinscripcion);
    (tramite(4), ver_servicio);
    (tramite(5), ver_titulacion).

iniciar:-
    preguntar_si_tramite,
    (realizando_tramite(1), menu_tramite, revisar_que_rollo_con_el_tramite);
    (realizando_tramite(2), menu_quedebohacer).

/*Proceso de preinscripción*/
ver_preinscripcion:-
    write("¿Presentaste tu examen de admision?"),nl,
    write( "1. si, 2. no"),
    read(Presento),
    retractall(presento_admision(_)), assertz(presento_admision(Presento)),nl,
    ((presento_admision(1), ver_aceptacion);
    (presento_admision(2), write("Para seguir con este tramite debes realizar el examen de admisión"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_preinscripcion)).

ver_aceptacion:-
    write("¿Sales en la lista de aceptados?"),nl,
    write( "1. si, 2. no"),
    read(Aceptado),
    retractall(lista_aceptados(_)), assertz(lista_aceptados(Aceptado)),nl,
    ((lista_aceptados(1), ver_cuota);
    (lista_aceptados(2), write("El proceso terminó para ti"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_aceptacion)).

ver_cuota:- write("¿Pagaste la cuota de los cursos?"),nl,
    write( "1. si, 2. no"),
    read(Cuota),
    retractall(cuota(_)), assertz(cuota(Cuota)),nl,
    ((cuota(1), ver_cursos);
    (cuota(2), write("Para seguir con este tramite debes pagar la cuota"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_cuota)).

ver_cursos:- write("¿Realizaste el curso propedeutico y de inducción?"),nl,
    write( "1. si, 2. no"),
    read(Cursos),
    retractall(cursos(_)), assertz(cursos(Cursos)),nl,
    ((cursos(1), ver_lista_aspirantes);
    (cursos(2), write("Para seguir con este tramite debes realizar los cursos"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_cursos)).

ver_lista_aspirantes:- write("¿Apareces en la lista de aspirantes seleccionados?"),nl,
    write( "1. si, 2. no"),
    read(Lista),
    retractall(lista_aspirantes(_)), assertz(lista_aspirantes(Lista)),nl,
    ((lista_aspirantes(1), write("Felicidades, estás preinscrito"));
    (lista_aspirantes(2), write("Alumno no seleccionado, vuelve en 6 meses"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_lista_aspirantes)).

/*proceso de inscripción*/
ver_inscripcion:- write("¿Estás preinscrito?"),nl,
    write( "1. si, 2. no"),
    read(Pre),
    retractall(preinscrito(_)), assertz(preinscrito(Pre)),nl,
    ((preinscrito(1), cuota_inscripcion);
    (preinscrito(2), write("Debes preinscribirte"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_inscripcion)).

cuota_inscripcion:-write("¿Pagaste la cuota de inscripción?"),nl,
    write( "1. si, 2. no"),
    read(Cuota),
    retractall(cuota(_)), assertz(cuota(Cuota)),nl,
    ((cuota(1), ver_documentacion);
    (cuota(2), write("Para seguir con este tramite debes pagar la cuota"));
    (write("La opción que ingresaste es incorrecta"), nl, cuota_inscripcion)).

ver_documentacion:- write("¿Entregaste la documentación?"),nl,
    write( "1. si, 2. no"),
    read(Docu),
    retractall(entrego_documentacion(_)), assertz(entrego_documentacion(Docu)),nl,
    ((entrego_documentacion(1), ver_aceptacion_docu);
    (entrego_documentacion(2), write("Para seguir con este tramite debes entregar los documentos solicitados."));
    (write("La opción que ingresaste es incorrecta"), nl, ver_documentacion)).

ver_aceptacion_docu:- write("¿Aceptaron tus documentos?"),nl,
    write( "1. si, 2. no"),
    read(Aceptacion),
    retractall(aceptacion_docu(_)), assertz(aceptacion_docu(Aceptacion)),nl,
    ((aceptacion_docu(1), write("Felicidades, estás inscrito"));
    (aceptacion_docu(2), write("Reenvía tus documentos con las correcciones"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_aceptacion_docu)).
/*Proceso de reinscripción*/
ver_reinscripcion:-write("¿Estás inscrito?"),nl,
    write( "1. si, 2. no"),
    read(I),
    retractall(inscrito(_)), assertz(inscrito(I)),nl,
    ((inscrito(1), ver_cuota_rein);
    (inscrito(2), write("Para seguir con este tramite debes estar inscrito"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_reinscripcion)).

ver_cuota_rein:-write("¿Pagaste la cuota del semestre?"),nl,
    write( "1. si, 2. no"),
    read(Cuota),
    retractall(cuota(_)), assertz(cuota(Cuota)),nl,
    ((cuota(1), ver_carga);
    (cuota(2), write("Para seguir con este tramite debes pagar la cuota del semestre"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_cuota_rein)).

ver_carga:-write("¿Hiciste la carga de materias?"),nl,
    write( "1. si, 2. no"),
    read(Cuota),
    retractall(cuota(_)), assertz(cuota(Cuota)),nl,
    ((cuota(1), ver_cursos);
    (cuota(2), write("Para seguir con este tramite debes pagar la cuota"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_cuota)).
/*Proceso de servicio social*/
ver_servicio:-write("¿Cumples con el 70% de los creditos?"),nl,
    write( "1. si, 2. no"),
    read(Cred),
    retractall(creditos(_)), assertz(creditos(Cred)),nl,
    ((creditos(1), ver_grupo);
    (creditos(2), write("Sigue progresando en tu reticula hasta que hayas completado el 70%"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_servicio)).

ver_grupo:-write("¿Estás en el grupo de facebook?"),nl,
    write( "1. si, 2. no"),
    read(G),
    retractall(grupo(_)), assertz(grupo(G)),nl,
    ((grupo(1), ver_induccion);
    (grupo(2), write("Debes unirte al grupo de facebook"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_grupo)).

ver_induccion:- write("¿Realizaste el curso de inducción al servicio social?"),nl,
    write( "1. si, 2. no"),
    read(Cursos),
    retractall(cursos(_)), assertz(cursos(Cursos)),nl,
    ((cursos(1), ver_registro_folio);
    (cursos(2), write("Para seguir con este tramite debes realizar el curso de inducción"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_induccion)). 

ver_registro_folio:-write("¿Registraste el folio del programa del registro social"),nl,
    write( "1. si, 2. no"),
    read(Folio),
    retractall(folio(_)), assertz(folio(Folio)),nl,
    ((folio(1), ver_carta);
    (folio(2), write("Para seguir con este tramite debes registrar el folio del programa"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_registro_folio)).

ver_carta:- write("¿Entregaste la carta de aceptación?"),nl,
    write( "1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), ver_entrega_reportes);
    (carta(2), write("Para seguir con este tramite debes entregar la carta de aceptación"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_carta)).

ver_entrega_reportes:- write("¿Entregaste los reportes 1,2,3?"),nl,
    write( "1. si, 2. no"),
    read(Rep),
    retractall(reportes(_)), assertz(reportes(Rep)),nl,
    ((reportes(1), ver_evaluacion);
    (reportes(2), write("Para seguir con este tramite debes entregar los reportes 1, 2 y 3 para continuar."));
    (write("La opción que ingresaste es incorrecta"), nl, ver_entrega_reportes)).

ver_evaluacion:- write("¿Entregaste la evaluación de actividades"),nl,
    write("1. si, 2. no"),
    read(Eva),
    retractall(evaluacion(_)), assertz(evaluacion(Eva)),nl,
    ((evaluacion(1), ver_terminacion);
    (evaluacion(2), write("Para seguir con este tramite debes entregar la evaluacion de actividades"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_evaluacion)).

ver_terminacion:- write("¿Entregaste la carta de terminación?"),nl,
    write("1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), ver_informe_final);
    (carta(2), write("Para seguir con este tramite debes entregar la carta de terminacion"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_terminacion)).

ver_informe_final:- write("¿Entregaste el informe final?"),nl,
    write( "1. si, 2. no"),
    read(Info),
    retractall(informe(_)), assertz(informe(Info)),nl,
    ((informe(1), ver_carta_liberacion);
    (informe(2), write("Para seguir con este tramite debes entregar el informe final"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_informe_final)).

ver_carta_liberacion:- write("¿recogiste la carta de liberación?"),nl,
    write( "1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), write("Ya terminaste con el proceso "));
    (carta(2), write("Ve y recoje la carta de aceptación"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_carta)).


ver_grupo:-write("¿Estás en el grupo de facebook?"),nl,
    write( "1. si, 2. no"),
    read(G),
    retractall(grupo(_)), assertz(grupo(G)),nl,
    ((grupo(1), ver_induccion);
    (grupo(2), write("Debes unirte al grupo de facebook"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_grupo)).

ver_induccion:- write("¿Realizaste el curso de inducción al servicio social?"),nl,
    write( "1. si, 2. no"),
    read(Cursos),
    retractall(cursos(_)), assertz(cursos(Cursos)),nl,
    ((cursos(1), ver_registro_folio);
    (cursos(2), write("Para seguir con este tramite debes realizar el curso de inducción"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_induccion)). 

ver_registro_folio:-write("¿Registraste el folio del programa del registro social"),nl,
    write( "1. si, 2. no"),
    read(Folio),
    retractall(folio(_)), assertz(folio(Folio)),nl,
    ((folio(1), ver_carta);
    (folio(2), write("Para seguir con este tramite debes registrar el folio del programa"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_registro_folio)).

ver_carta:- write("¿Entregaste la carta de aceptación?"),nl,
    write( "1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), ver_entrega_reportes);
    (carta(2), write("Para seguir con este tramite debes entregar la carta de aceptación"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_carta)).

ver_entrega_reportes:- write("¿Entregaste los reportes 1,2,3?"),nl,
    write( "1. si, 2. no"),
    read(Rep),
    retractall(reportes(_)), assertz(reportes(Rep)),nl,
    ((carta(1), ver_evaluacion);
    (carta(2), write("Para seguir con este tramite debes entregar los reportes 1, 2 y 3 para continuar."));
    (write("La opción que ingresaste es incorrecta"), nl, ver_entrega_reportes)).

ver_evaluacion:- write("¿Entregaste la evaluación de actividades"),nl,
    write("1. si, 2. no"),
    read(Eva),
    retractall(evaluacion(_)), assertz(evaluacion(Eva)),nl,
    ((carta(1), ver_terminacion);
    (carta(2), write("Para seguir con este tramite debes entregar la evaluacion de actividades"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_evaluacion)).

ver_terminacion:- write("¿Entregaste la carta de terminación?"),nl,
    write("1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), ver_informe_final);
    (carta(2), write("Para seguir con este tramite debes entregar la carta de terminacion"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_terminacion)).

ver_informe_final:- write("¿Entregaste el informe final?"),nl,
    write( "1. si, 2. no"),
    read(Info),
    retractall(informe(_)), assertz(informe(Info)),nl,
    ((carta(1), ver_carta_liberacion);
    (carta(2), write("Para seguir con este tramite debes entregar el informe final"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_informe_final)).

ver_carta_liberacion:- write("¿recogiste la carta de liberación?"),nl,
    write( "1. si, 2. no"),
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)),nl,
    ((carta(1), write("Ya terminaste con el proceso "));
    (carta(2), write("Ve y recoje la carta de aceptación"));
    (write("La opción que ingresaste es incorrecta"), nl, ver_carta)).


/*Proceso titulacion*/
ver_titulacion :-
    write("¿Reuniste todos los requisitos para titularte?"), nl,
    write("1. si, 2. no"), nl,
    read(Requisitos),
    retractall(creditos(_)), assertz(creditos(Requisitos)), nl,
    ((creditos(1), ver_opcion_titulacion);
     (creditos(2), write("Debes reunir todos los requisitos para poder titularte"));
     (write("Opción incorrecta"), nl, ver_titulacion)).

ver_opcion_titulacion :-
    write("¿Acreditaste la opción de titulación de tu plan de estudios?"), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    retractall(cursos(_)), assertz(cursos(Opcion)), nl,
    ((cursos(1), ver_cita_cotejo);
     (cursos(2), write("Debes acreditar una opción de titulación para continuar"));
     (write("Opción incorrecta"), nl, ver_opcion_titulacion)).

ver_cita_cotejo :-
    write("¿Solicitaste la cita para el cotejo de documentos?"), nl,
    write("1. si, 2. no"), nl,
    read(Cita),
    retractall(folio(_)), assertz(folio(Cita)), nl,
    ((folio(1), ver_carta_no_inconveniencia);
     (folio(2), write("Debes solicitar tu cita para continuar"));
     (write("Opción incorrecta"), nl, ver_cita_cotejo)).

ver_carta_no_inconveniencia :-
    write("¿Recogiste la carta de no inconveniencia?"), nl,
    write("1. si, 2. no"), nl,
    read(Carta),
    retractall(carta(_)), assertz(carta(Carta)), nl,
    ((carta(1), ver_acto_formalizacion);
     (carta(2), write("Debes recoger la carta de no inconveniencia"));
     (write("Opción incorrecta"), nl, ver_carta_no_inconveniencia)).

ver_acto_formalizacion :-
    write("¿Asististe al acto de formalización?"), nl,
    write("1. si, 2. no"), nl,
    read(Acto),
    retractall(reportes(_)), assertz(reportes(Acto)), nl,
    ((reportes(1), ver_juramento);
     (reportes(2), write("Debes asistir al acto de formalización"));
     (write("Opción incorrecta"), nl, ver_acto_formalizacion)).

ver_juramento :-
    write("¿Realizaste la toma de juramento?"), nl,
    write("1. si, 2. no"), nl,
    read(Juramento),
    retractall(evaluacion(_)), assertz(evaluacion(Juramento)), nl,
    ((evaluacion(1), ver_registro_titulo);
     (evaluacion(2), write("Debes realizar la toma de juramento"));
     (write("Opción incorrecta"), nl, ver_juramento)).

ver_registro_titulo :-
    write("¿Registraste tu título?"), nl,
    write("1. si, 2. no"), nl,
    read(Registro),
    retractall(informe(_)), assertz(informe(Registro)), nl,
    ((informe(1), ver_expedicion_cedula);
     (informe(2), write("Debes registrar tu título para continuar"));
     (write("Opción incorrecta"), nl, ver_registro_titulo)).

ver_expedicion_cedula :-
    write("¿Ya te expidieron la cédula profesional?"), nl,
    write("1. si, 2. no"), nl,
    read(Cedula),
    retractall(grupo(_)), assertz(grupo(Cedula)), nl,
    ((grupo(1), write("¡Felicidades! Has concluido tu proceso de titulación."));
     (grupo(2), write("Debes esperar la expedición de tu cédula profesional"));
     (write("Opción incorrecta"), nl, ver_expedicion_cedula)).

menu_quedebohacer :-
    preguntar_recien_egresado.

preguntar_recien_egresado :-
    write("¿Eres recién egresado de preparatoria?"), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 1 ->
        assertz(recien_egresado),
        write("Debes hacer el trámite de preinscripción."), nl
    ; Opcion == 2 ->
        assertz(no_recien_egresado),
        preguntar_inscrito
    ; write("Opción no válida."), nl, preguntar_recien_egresado).

preguntar_inscrito :-
    write("¿Estás inscrito actualmente?"), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 2 ->
        assertz(no_inscrito),
        write("Debes hacer el trámite de inscripción."), nl
    ; Opcion == 1 ->
        assertz(inscrito),
        preguntar_en_vacaciones
    ; write("Opción no válida."), nl, preguntar_inscrito).

preguntar_en_vacaciones :-
    write("¿Estás en periodo vacacional? "), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 1 ->
        assertz(en_vacaciones),
        write("Debes hacer el trámite de reinscripción."), nl
    ; Opcion == 2 ->
        assertz(no_en_vacaciones),
        preguntar_semestre
    ; write("Opción no válida."), nl, preguntar_en_vacaciones).

preguntar_semestre :-
    write("¿En qué semestre estás? (Número entero)"), nl,
    read(Semestre),
    assertz(semestre(Semestre)),
    (Semestre < 7 ->
        write("Alumno no debe realizar ningún trámite por el momento."), nl
    ; preguntar_creditos).

preguntar_creditos :-
    write("¿Qué porcentaje de créditos has completado? (0-100)"), nl,
    read(Creditos),
    assertz(creditos(Creditos)),
    (Creditos < 70 ->
        write("Alumno no debe realizar ningún trámite por el momento."), nl
    ; Creditos < 100 ->
        write("Debes iniciar tu servicio social."), nl
    ; preguntar_lengua).

preguntar_lengua :-
    write("¿Ya acreditaste la lengua extranjera? "), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 2 ->
        write("Aún no puedes tramitar tu título. Te falta acreditar la lengua extranjera."), nl
    ; Opcion == 1 ->
        assertz(acredito_lengua),
        preguntar_servicio_social
    ; write("Opción no válida."), nl, preguntar_lengua).

preguntar_servicio_social :-
    write("¿Ya realizaste tu servicio social? "), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 2 ->
        write("Aún no puedes tramitar tu título. Te falta el servicio social."), nl
    ; Opcion == 1 ->
        assertz(realizo_servicio_social),
        preguntar_practicas
    ; write("Opción no válida."), nl, preguntar_servicio_social).

preguntar_practicas :-
    write("¿Ya realizaste tus prácticas profesionales? "), nl,
    write("1. si, 2. no"), nl,
    read(Opcion),
    (Opcion == 2 ->
        write("Aún no puedes tramitar tu título. Te faltan las prácticas profesionales."), nl
    ; Opcion == 1 ->
        assertz(realizo_practicas),
        write("Debes realizar el trámite de titulación."), nl
    ; write("Opción no válida."), nl, preguntar_practicas).
