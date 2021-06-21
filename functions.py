
data_collect_function = """function a() {
           var rows =  document.querySelectorAll("tbody > tr");
           var links = []
           for(var i = 0; i < rows.length; i++) {
                var date = rows[i].querySelector("span").textContent;

                var link = rows[i].querySelector("a").href;
                var content = rows[i].querySelector("td:nth-child(2)").textContent.trim();
                
                links.push({"date" : date, "link": link, "content" : content})
           }
           return links;
        }

        return a();"""

pick_date_function = """function a(){
    pick = document.querySelector("a[href='/en/news-events/whats-new/[dynamic]']")
    pick.click();
}
a();"""

load_page_function = """function a() {
          load = document.querySelector("body main div div section div div ul li a");
          load.click();
       }
a();"""

total_rows_function = """function a(){
    rows = document.getElementsByTagName('tr').length;
    return rows;
}
return a();"""

total_result_function = """return document.querySelector("a[href='/en/news-events/whats-new/[dynamic]'] > span").textContent.trim();"""