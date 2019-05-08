class Comic:

    def __init__(self, id_comic, month, num, link, year, news, 
                 safe_title, transcript, alt, img, title, day):
        self.id_comic = id_comic
        self.month = month
        self.num = num
        self.link = link
        self.year = year
        self.news = news
        self.safe_title = safe_title
        self.transcript = transcript
        self.alt = alt
        self.img = img
        self.title = title
        self.day = day

    def max_sql(self):
        return "select max(ID) 'm' from main.COMIC"

    def insert_sql(self):
        return '''
               insert 
                 into main.COMIC ("MONTH", "NUM", "LINK", "YEAR",
                                  "NEWS", "SAFE_TITLE", "TRANSCRIPT",
                                  "ALT", "IMG", "TITLE", "DAY") 
               values (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?)
               '''

    def insert_tuple(self):
        return (self.month, self.num, self.link, self.year, self.news, 
                self.safe_title, self.transcript, self.alt, self.img, 
                self.title, self.day)

    def update_sql(self):
        return '''
               update main.COMIC 
                  set "MONTH" = ?, NUM = ?, LINK = ?,  "YEAR" = ?, 
                      NEWS = ?, SAFE_TITLE = ?, TRANSCRIPT = ?, 
                      ALT = ?, IMG = ?, TITLE = ?, "DAY" = ? 
                where ID = ?
               '''

    def update_tuple(self):
        return (self.month, self.num, self.link, self.year, self.news, 
                self.safe_title, self.transcript, self.alt, self.img, 
                self.title, self.day, self.id_comic)

    def search_sql(self):
        return '''
               select * 
                 from main.COMIC 
                where lower(TRANSCRIPT) like ?
                   or lower(SAFE_TITLE) like ?
               '''

    def to_dict(self):
        return self.__dict__

    def delete_sql(self):
        return '''
               delete 
                 from main.COMIC
                where ID = ?
               '''

    def delete_tuple(self):
        return (self.id_comic, )
