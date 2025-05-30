from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import pandas as pd
from docxtpl import DocxTemplate
import datetime
import os

class CertificateGenerator(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        self.file_label = Label(text="No file selected") #adding upload to get xls file
        layout.add_widget(self.file_label)
        
        file_chooser = FileChooserListView()
        file_chooser.filters = ['*.xls', '*.xlsx']
        layout.add_widget(file_chooser)
        
        upload_button = Button(text="Generate Certificate", size_hint=(None, None), size=(200, 50))
        upload_button.bind(on_press=lambda x: self.generate_certificates(file_chooser.path, file_chooser.selection))
        layout.add_widget(upload_button)
        
        return layout
    
    def generate_certificates(self, path, filename):
        if filename:
            selected_file = filename[0]
            self.file_label.text = f"Selected file: {selected_file}" 
            try:
                df = pd.read_excel(selected_file)
                for index, row in df.iterrows():
                    today_date = datetime.datetime.today().strftime('%B %d %y')
                    name = row['NAME']
                    reg_no = row['PIN']
                    college = row['COLLEGE']
                    branch = row['BRANCH']
                    domain = row['DOMAIN']
                    st_date = row['START_DATE']
                    en_date = row['END_DATE']
                    internship_cord = row['InternshipCoordinator']
                    gender = row["GENDER"]
                    if(gender == "Male"):
                        gender="Mr"
                        gender1 = "He"
                    else:
                        gender = "Ms"
                        gender1 = "She"
                    self.generate_certificate(name, reg_no, branch, college, domain ,st_date, en_date, internship_cord, today_date, gender,gender1)
                print("Certificates generated successfully.") 
            except Exception as e:
                print("Error generating Certificate:", e)
        else:
            self.file_label.text = "No file selected"
    
    def generate_certificate(self, name, reg_no, branch, college,domain , st_date, en_date, inteship_cord , today_date,gender,gender1):
        folder_path = os.path.join('Certificates', college, branch, domain)
        os.makedirs(folder_path, exist_ok=True)
        certificate_filename = f'certificate_{name}.docx'
        certificate_path = os.path.join(folder_path, certificate_filename)

        st_date = st_date.strftime("%B-%m-%y")
        en_date = en_date.strftime("%B-%m-%y")
        context = {
        'today_date' : today_date,
        'name' : name,
        'branch' : branch,
        'college' : college,
        'domain' : domain,
        'reg_no' : reg_no,
        'internship_cord' : inteship_cord,
        'st_date' : st_date,
        'en_date' : en_date,
        'gender' : gender,
        'gender1' :gender1
        }
        doc = DocxTemplate("template_certificate.docx")//template_path

        doc.render(context)

        doc.save(certificate_path)
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # popup = Popup(title=f'Offer Letter for {name}', content=popup_layout, size_hint=(None, None), size=(400, 300))
        

        # close_button = Button(text='Close')
        # close_button.bind(on_press=popup.dismiss)
        # popup_layout.add_widget(close_button)
        
        # # popup.open()

if __name__ == '__main__':
    CertificateGenerator().run()

