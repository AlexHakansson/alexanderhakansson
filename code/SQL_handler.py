import mysql.connector
import pandas as pd






class sql_ob:

    def __init__(self, usr = 'root',psw='password',hst='127.0.0.1'):
    
    
        self.usr =usr
        self.hst = hst
        self.psw = psw
    
        self.cnx = mysql.connector.connect(user=usr, password=psw,
                                      host=hst,
                                     database='academicworld')
        self.cursor =  self.cnx.cursor()
        

        
        #add indexes for faster look up of keywords and profs
        self.cursor.execute("show index from keyword")
        keyword_ind =  pd.DataFrame(self.cursor.fetchall())
        if "kwrd_nm" not in list(keyword_ind.iloc[:,2]):
            print("making keyword index")
            self.cursor.execute("create index kwrd_nm on keyword(name)")
            print("finished")
        self.cursor.execute("show index from faculty")
        fac_ind =  pd.DataFrame(self.cursor.fetchall())
        if "fac_nm" not in list(fac_ind.iloc[:,2]):
            print("making faculty index")
            self.cursor.execute("create index fac_nm on faculty(name)")
            print("finished")
        #get keywords and profs for later (do it for this db just in case)
        self.cursor.execute("select distinct name from faculty")
        self.fac_nm = [x[0] for x in self.cursor.fetchall()]
        
        self.cursor.execute("select distinct name from keyword where id in (select keyword_id from faculty_keyword)")
        self.key_nm = [x[0] for x in self.cursor.fetchall()]
        
        self.fav_prof = []
        
        self.cursor.close()
        self.cnx.close()
        #print("Creating Favorites")
        #create_favorites(self.cursor)
        #print("Finished")
        
    def sql_connect(self):
        self.cnx = mysql.connector.connect(user=self.usr, password=self.psw,
                                      host=self.hst,
                                     database='academicworld')
        self.cursor =  self.cnx.cursor()
        
    def sql_disconnect(self):
        self.cursor.close()
        self.cnx.close()
    
    
    def create_favorites_2(self,fav_names=[]):
        
        self.sql_connect()
        
        coloi = ["id", "name","position", "research_interest","email","phone","photo_url","university_id"]
        coloi_alias = ", ".join([x + " as f_"+x for x in coloi])
        


        fav_string = "('" +"','".join(fav_names) +"')"
        #print(fav_string)
        create_view = ("create or replace view favorites as select * from (select " +
                       coloi_alias + " from faculty where name in "+ fav_string + ") as f " +
                      "left join university on university.id=f_university_id")
        #print(create)
        self.cursor.execute(create_view)
        self.cursor.fetchall()
        
        #self.cursor.execute("describe favorites")
        #print(self.cursor.fetchall())
        
        coi_final = ["f_name","name","f_position","f_email","f_phone"]
        self.cursor.execute("select "+",".join(coi_final)+" from favorites")
        tbl = self.cursor.fetchall()
        if len(tbl) >0:
            tbl = pd.DataFrame(tbl)
            tbl.columns = coi_final
            self.fav_prof = list(tbl.loc[:,"f_name"])
        else:
            tbl = pd.DataFrame(columns=coi_final)
            self.fav_prof = []
        #cursor.close()
        self.sql_disconnect()
        return(tbl)
        
    def select_top_faculty_by_keyword(self, key_wrd,lim=10):
        #cursor =  cnx_ob.cursor()
        self.sql_connect()
        query = ("select name, score from " + "(select faculty_id, score from faculty_keyword where keyword_id="+
             "(select id as kid from keyword where name='"+key_wrd+"') order by score desc limit "+
               str(lim) +") as test "+
             "inner join faculty on faculty.id=faculty_id")
        self.cursor.execute(query)
        
        vals = self.cursor.fetchall()
        vals = pd.DataFrame(vals)
        vals.columns =["name","score"]
        self.sql_disconnect()
        
        return vals
                                          
    
    def select_top_keyword_by_faculty(self,faculty,lim=10):
        #cursor =  cnx_ob.cursor()
        self.sql_connect()
        query = ("select name, score from " + "(select keyword_id, score from faculty_keyword where faculty_id="+
             "(select id as fid from faculty where name='"+faculty+"') order by score desc limit "+
               str(lim) +") as test "+
             "inner join keyword on keyword.id=keyword_id")
        self.cursor.execute(query)
        
        vals = self.cursor.fetchall()
        vals = pd.DataFrame(vals)
        vals.columns =["keyword","score"]
        
        self.cursor.close()
        
        return vals    
        
    def read_fav_table(self):
        self.sql_connect()
        coi_final = ["f_name","name","f_position","f_email","f_phone"]
        self.cursor.execute("select "+",".join(coi_final)+" from favorites")
        tbl = self.cursor.fetchall()
        if len(tbl) >0:
            tbl = pd.DataFrame(tbl)
            tbl.columns = coi_final
        else:
            tbl = pd.DataFrame(columns=coi_final)
        #cursor.close()
        self.sql_disconnect()
        return(tbl)
        
        
    def compare_favorites(self,key_wrd,lim=20):
    
        self.sql_connect()
        query = ("select name, score from " + "(select faculty_id, score from faculty_keyword where keyword_id="+
             "(select id as kid from keyword where name='"+key_wrd+"') "+
             "and faculty_id in (select f_id from favorites) order by score desc limit "+
               str(lim) +") as test "+ "inner join faculty on faculty.id=faculty_id")
        self.cursor.execute(query)
        
        vals = self.cursor.fetchall()
        vals = pd.DataFrame(vals)
        vals.columns =["name","score"]
        self.sql_disconnect()
        
        return vals
                          