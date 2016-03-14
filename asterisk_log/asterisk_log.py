#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#
#                     Module [asterisk_log] MLMConseil
#                    ----------------------------------
#
#                    ----------------------------------
#                   permet de recharger les appels d'asterisk
#                   par le fichier "Master.csv" 
#                  ----------------------------------------
#                       langage : Python 2.7
#                       date creation : 30/10/2015
#                       date modification : /2015
#                       version : 0.1
#                       auteur  : MLMconseil
#
################################################################################
from openerp.osv import fields, osv, orm
import logging
import datetime
import time
import sys, os

_logger = logging.getLogger(__name__)

# chemin absolu vers le fichier Master.csv
PATH_MASTER = 'C:\\Program Files (x86)\\Odoo 8.0-20150719\\server\\openerp\\addons\\asterisk_log\\Master.csv' 
#liste des numero de telephone de l'entreprise , pour distinguer les appels entrants et sortants
LIST_PHONE = ['0043434343434','034567812323']
class asterisk_log(osv.Model):
    _name = 'asterisk.log'
    _description = "Informations sur les appels"
    _order = 'date' #'date desc'  DESC
    _log_access = False

    _columns = {
        #'name': fields.many2one('res.partner', 'Nom'), 
        'appelant': fields.char('Appelant', size=50), #, required=True
        'appele': fields.char('Appelé', size=50),
        'date': fields.char('Date', size=50),
        'heure' : fields.char('Heure', size=50),
        'duree': fields.char('Durée', size=50),
        'etat': fields.char('Etat', size=50),
        #'total_appel': fields.function(_appel_total, string='total d\'appel', type='integer'),
    }

    def update_tree(self, cr, uid, ids, context=None):
        i = 0
        ligne_file = 0
        max_id = 0
        req = None
        try:
            date_mnt = time.strftime("%d-%m-%Y")
            req1 = "SELECT count(*) FROM asterisk_log" #" SELECT COUNT(*) FROM asterisk_log"
            cr.execute(req1)
            id_appel = cr.fetchone()[0]
            if id_appel == None:
				id_appel = 0
            max_id = id_appel
            try:
                file = open(PATH_MASTER,'r')
            except IOError:
                raise orm.except_orm(("Erreur :"),("fichier Master.csv introuvable %s" % (os.path.abspath(PATH_MASTER))))
                # sys.exit(0)

            for ligne in file.readlines():
                if ligne_file > max_id-2: #changer a max_id-1
                    i +=1
                    appelant = str(ligne.split(",")[4].replace('"','')) # recupere au format Merouane <208>
                    appele = str(ligne.split(",")[2].replace('"',''))
                    #dans le cas ou c un appel entrant
                    if appele in LIST_PHONE:
                        appelant = str(ligne.split(",")[1].replace('"','')) # recuperer juste le num
                        date_heure = len(ligne.split(",")[13].replace('"','').split(" "))
                        if date_heure == 2:
                    		date = str(ligne.split(",")[13].replace('"','').split(" ")[0])
                    		heure = str(ligne.split(",")[13].replace('"','').split(" ")[1])
                    	else:
                    		date = str(ligne.split(",")[13].replace('"',''))
                    		heure = '00:00:00'
                    	duree = str(ligne.split(",")[15].replace('"',''))
                    	etat = str(ligne.split(",")[16].replace('"',''))
                        id_appel +=1
                        req = "INSERT INTO asterisk_log(appelant, appele, date, heure, duree, etat)  \
                                            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}' \
                                                )".format(appelant, appele, date, heure, duree, etat)


                     ##dans le cas ou c un appel sortant
                    else:
                        date_heure = len(ligne.split(",")[9].replace('"','').split(" "))
                        if date_heure == 2:
                			date = str(ligne.split(",")[9].replace('"','').split(" ")[0])
                			heure = str(ligne.split(",")[9].replace('"','').split(" ")[1])
                        else:
                			date = str(ligne.split(",")[9].replace('"',''))
                			heure = '00:00:00'
                        duree = str(ligne.split(",")[13].replace('"',''))
                        etat = str(ligne.split(",")[14].replace('"',''))

                    	id_appel +=1
                    	req = "INSERT INTO asterisk_log(appelant, appele, date, heure, duree, etat)  \
                                                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}' \
                                                    )".format(appelant, appele, date, heure, duree, etat)

                    cr.execute(req)
                    cr.commit()
                ligne_file +=1
            file.close

        except Exception as err:
        	raise orm.except_orm(
				("Erreur :"),
                ("requete incorrecte  ! \n details :  %s \n req = %s" % (err, req)))
        else:
        	if i==0:
				raise orm.except_orm(("Mise à jour"),
					("Pas de nouvels appels"))
        	else:
				raise orm.except_orm(
					("Mise à jour reussie"),
            		("%s  Nouvels appels trouvés" % i))

        finally:
            _logger.info("Mise a jour des appels reussie: %s appels trouvé" % i)
