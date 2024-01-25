Our Project Structure Cantains:

Base_Dir:
    
    In the Base_Dir contains
        i) Apps

            It Contains all the apps of our project except "accounts"


        ii) static
            It Contains all the static files of our project
    
        iii) templates

            The template contains

                i) includes
                    it contains  all the include files that are use in base.html


                ii) utils
                    the utils contains all the utils like (messages.html, 404.html, 500.html, list_icons.html)


                iii) base.html
                     base.html is the Parent file for our project



APPS_TEMPLATES_INFORMATION:

        In evry app in App folder conatins templates folder

        templates folder contains:

            i) folder with name same as app name:

                inside this  folder :
                    i) two files   (model_add.html, model_list.html):
                        
                        this tow file will be inherit form the base.html and include the correspoind file form the partials folder

                    ii) one folder  (partials):

                        this folder also conatins tow partial files (model_add.html, model_list.html)
            
            Remember:
                    core app structure is defferent from the above




Core App Template Structure:

    it contains templates folder:

    templates folder:

        as in this core app we have alot of models so we create a sperate folder inside the templates folder for every model in the core app with the same name as model name

        now that model name folder will be the same structure as our project template structure


