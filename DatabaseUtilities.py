import pymysql.cursors

class DatabaseUtilities():

    def __init__(self):
        #TODO: place the Python dictionary in charge of credentials here
        #TODO: place credentials in the environmental variables
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='pass',
                             db='picnote',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    ''' Methods for reading course information '''
    def read_professor_id(self,username,password):
        '''
        Method that reads the professor id of the given professor based on their username and password
        :param username: String
        :param password: String
        :return: id: Integer
        '''
        try:
            #Creates the database cursor responsibile for executing query and extracting data
            with self.connection.cursor() as cursor:
                sql = "SELECT PROF_ID FROM PROFESSOR WHERE USERNAME = %s AND PWD = %s"
                cursor.execute(sql,(username,password))
                #Obtains all of the data from the query
                results = cursor.fetchall()


        except Exception as e:
            print(e)
            #Catches the exceptions thrown by database errors
            results ={"Error":"Could not retrieve JOBS from the database"}

        finally:
            #Returns the result of the query or error message
            return results

    def read_notes_by_section(self, section_id):
        '''
        Method that reads notes for section
        :param section_id: the id of the section
        '''
        try:
            # Creates the database cursor responsibile for executing query and extracting data
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM NOTE WHERE FK_SECTION_NOTE = %s"
                cursor.execute(sql, (section_id))
                # Obtains all of the data from the query
                results = cursor.fetchall()

        except Exception as e:
            print(e)
            # Catches the exceptions thrown by database errors
            results = {"Error": "Could not retrieve JOBS from the database"}

        finally:
            # Returns the result of the query or error message
            return results

    def read_notes_by_course(self, course_id):
        '''
        Method that reads notes for a course
        :param course_id: the id of a course
        '''
        try:
            # Creates the database cursor responsibile for executing query and extracting data
            with self.connection.cursor() as cursor:
                sql = "SELECT NOTE.* FROM NOTE " \
                      "INNER JOIN SECTION ON NOTE.FK_SECTION_NOTE = SECTION.SECTION_ID " \
                      "WHERE SECTION.FK_COURSE_SECTION= %s"
                cursor.execute(sql, (course_id))
                # Obtains all of the data from the query
                results = cursor.fetchall()

        except Exception as e:
            print(e)
            # Catches the exceptions thrown by database errors
            results = {"Error": "Could not retrieve JOBS from the database"}

        finally:
            # Returns the result of the query or error message
            return results

    def read_notes_by_prof(self, prof_id):
        '''
        Method that reads notes by specific professor
        :param prof_id: the id of the professor
        '''
        try:
            # Creates the database cursor responsibile for executing query and extracting data
            with self.connection.cursor() as cursor:
                sql = "SELECT NOTE.* FROM NOTE " \
                      "INNER JOIN SECTION ON NOTE.FK_SECTION_NOTE = SECTION.SECTION_ID " \
                      "INNER JOIN COURSE ON SECTION.FK_COURSE_SECTION = COURSE.COURSE_ID " \
                      "WHERE COURSE.FK_PROFESSOR_COURSE= %s"
                cursor.execute(sql, (prof_id))
                # Obtains all of the data from the query
                results = cursor.fetchall()

        except Exception as e:
            print(e)
            # Catches the exceptions thrown by database errors
            results = {"Error": "Could not retrieve JOBS from the database"}

        finally:
            # Returns the result of the query or error message
            return results

    ''' Methods to write course information '''
    def write_course_entry(self, class_name,prof_id):
        pass
        #TODO: Put SQL query to write course

    def write_section_entry(self, course_id,section_name):
        pass
        #TODO: Put SQL query to write section

    def write_note_entry(self,desc,img,section_id):
        pass
        # TODO: Put SQL query to write section


if __name__=="__main__":
    dbu = DatabaseUtilities()
    print(dbu.read_professor_id("PATTIS","ONELINE"))
    print(dbu.read_notes_by_section(1))
    print(dbu.read_notes_by_course(2))
    print(dbu.read_notes_by_prof(2))