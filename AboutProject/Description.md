PRELOADER:
    i) we add some style for preloader in base.html with (inner style) on the top of the base.html.

    ii) then we add hx-indicator attribute that will inherite by all of it's childs so we do not need to 
    aplay them to all other childs.

    iii) As some partials not inherit it's parent hx-attribute then me manualy add them on row in that partials. partials include uptil is (circle_list.html).


MESSAGES (toast):

    i) for messages we create a separate html file in utils with the name "messages.html" that contain code 
        showing toas messages
    
    ii) then we include them on evary page in the partials



MAXLENTGTH_BADGE:

    i) add mxalength.js in base.html
    ii) then add maxlen.html to input partials from utils in templates on Base_Dir 


INPUT_MASK:

    i) add s main inputmask.js file in base.html (actual maskfile).
    
    ii) then we add above file in all the input partials where we need them
    becuase this arise error "jquay is not define".
    
    iii) then we iniialize the inputmask by ading inputmask.html from utils in both base.html and 
    all the input partials.
       