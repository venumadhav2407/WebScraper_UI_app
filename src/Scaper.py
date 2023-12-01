import requests 
from bs4 import BeautifulSoup
import customtkinter as ctk
import re
import csv
from tkinter import filedialog, messagebox


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")


# venv\Lib\site-packages\customtkinter\windows\widgets\theme
# venv\Lib\site-packages\customtkinter\assets\themes





class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        
        self.title("Web Scraper")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.label = ctk.CTkLabel(self, text="WEB SCRAPER", text_color="#DE3924", font=('poppins', 45))
        self.label.grid(row=0, column=1)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Entet the URL", placeholder_text_color="#808080", height=35)
        self.entry.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10,5))
        
        self.btn = ctk.CTkButton(self, text="Scrape", width=60, height=35, font=('poppins', 15), command=self.scrape)
        self.btn.grid(row=1, column=2)
        
        self.clearbt = ctk.CTkButton(self,text="Clear", width=60, height=35, font=('poppins', 15), command=self.clear)
        self.clearbt.grid(row=1, column=3)
    
        self.menu = ctk.CTkOptionMenu(self, values=['Extract All','Title', 'Heading','Div', 'links', 'Image Links'], hover=True)
        self.menu.grid(row=2, column=2,padx=(10,10), pady=(10,10))
        
        
        self.convert = ctk.CTkButton(self, text="Save as csv", width=120, height=35, font=('poppins', 25), command=self.convert_to_csv)
        self.convert.grid(row=4, column=2)
        
        self.textB = ctk.CTkTextbox(self, width=400, height=600, state='disabled')
        self.textB.grid(row=4, column=1,padx=10, sticky="nsew")
        
    #     self.textB.bind("<<TextModified>>",command=self.enable_save_button)
        
        
    # def enable_save_button(self, even):
    #     if self.textB.get("1.0", "end-1c") ==:
    #         self.convert.configure(state="normal")
    #     else:
    #         self.convert.configure(state="disabled")
        
        
       
    def clear(self):
        self.textB.configure(state="normal")
        self.textB.delete("1.0", ctk.END)
        
                
        
    def scrape(self):
        self.url = self.entry.get()
        
        
        
        if self.url == "":
            messagebox.showwarning(title="Input Field", message="Provide the URL please!!")
        else:
            
            
            self.response = requests.get(self.url)
            
            self.soup = BeautifulSoup(self.response.content, "html.parser")
            
            # pattern
            self.pattern = r"www\..+?\.com"
            
            
            self.textB.configure(state='normal')
            self.textB.delete("1.0", ctk.END)
            
            # get value
            self.val = self.menu.get()
            
            if self.val == 'Title':
                self.textB.insert('end', self.soup.title.text + '\n')
            elif self.val == 'Heading':
                self.textB.insert('end', self.soup.h1.text + '\n')
            elif self.val == 'Div':
                self.divs = self.soup.find_all('div')
                for div in self.divs:
                    self.textB.insert('end', div.prettify() )
            elif self.val == "links":
                self.links = self.soup.find_all('a')
                for link in self.links:
                    self.href = link.get('href')
                    if self.href and re.search(self.pattern, self.href):
                        self.textB.insert('end', self.href + '\n')
            elif self.val == "Extract All":
                self.textB.insert('end', self.soup.prettify())

            elif self.val == "Image Links":
                self.img =  self.soup.find_all('img')
                # self.pattern1 = r'<img.*?src="(https.*?)".*?>'
                for src in self.img:
                    self.src = src.get('src')
                    if self.src: # and re.search(self.pattern1, self.src):
                        self.textB.insert('end', self.src + '\n')
            
                    
            # self.textB.insert('end', 'links: \n')
            # self.textB.insert('end', self.data + '\n')
            
            self.textB.configure(state='disabled')
                
                
    # Convert data to CSV
    def convert_to_csv(self):
        # if self.val == 'Title':
        #     filename = "Title.csv"
        # elif self.val == "Heading":
        #     filename = "Heading.csv"
        # elif self.val == "Div":
        #     filename = "Div.csv"
        # elif self.val == "links":
        #     filename = "links.csv"
        # elif self.val == "Image Links":
        #     filename = "Images.csv"
        # else:
        #     filename = "Data.csv"
            
            
        filename = filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(file=filename.name, mode='w', newline='') as file:
                writer = csv.writer(file)
                if self.val == 'Title':
                    writer.writerow([self.soup.title.text])
                elif self.val == 'Heading':
                    writer.writerow([self.soup.h1.text])
                elif self.val == 'Div':
                    self.divs = self.soup.find_all('div')
                    for div in self.divs:
                        writer.writerow([div.prettify()])
                elif self.val == "links":
                    self.links = self.soup.find_all('a')
                    for link in self.links:
                        self.href = link.get('href')
                        if self.href and re.search(self.pattern, self.href):
                            writer.writerow([self.href])
                elif self.val == "Extract All":
                    writer.writerow([self.soup.prettify()])
                elif self.val == "Image Links":
                    self.img =  self.soup.find_all('img')
                    for src in self.img:
                        self.src = src.get('src')
                        if self.src:
                            writer.writerow([self.src])
            messagebox.showinfo(title="File Saved", message=f"File saved at: {filename.name}")
        
    # def covert_to_spreadSheet():
        # pass








if __name__ == "__main__":
    app = App()
    app.mainloop()