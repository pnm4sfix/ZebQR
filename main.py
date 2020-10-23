# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:03:38 2020

@author: pierc
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
import os
import qrcode

KV = '''

BoxLayout:
    shoal: shoal_id
    fish_num: fish_number
    dobs: dob
    strains: strain
    image: image
    
    orientation:'vertical'
    Image:
        id: image
        #source: 'mylogo.png'
        #size: self.texture_size
    
    MDTextField:
        id: shoal_id
        hint_text: "Whats the shoal ID?"
        #helper_text: "This will disappear when you click off"
        helper_text_mode: "on_focus"
        pos_hint: {"center_x": .5, "center_y": .1}
        #text: root.shoal
        padding_x:
            [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,
            0] if self.text else [self.center[0], 0]
        
    MDTextField:
        id: fish_number
        hint_text: "Number of fish"
        #helper_text: "This will disappear when you click off"
        helper_text_mode: "on_focus"
        pos_hint: {"center_x": .5, "center_y": .25}
        #text: root.fish_num
        padding_x:
            [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,
            0] if self.text else [self.center[0], 0]
        
    MDTextField:
        id: dob
        hint_text: "Date of hatching?"
        #helper_text: "This will disappear when you click off"
        helper_text_mode: "on_focus"
        pos_hint: {"center_x": .5, "center_y": .4}
        padding_x:
            [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,
            0] if self.text else [self.center[0], 0]
    
        
    MDTextField:
        id: strain
        hint_text: "What strain?"
        #helper_text: "This will disappear when you click off"
        helper_text_mode: "on_focus"
        pos_hint: {"center_x": .5, "center_y": .55}
        padding_x:
            [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,
            0] if self.text else [self.center[0], 0]
    
    MDRaisedButton:
        text: "Create QR Code"
        #text_color: 0, 0, 1, 1
        pos_hint: {"center_x": .5, "center_y": .8}
        on_press: app.create_qr()
            
            
            
    
    '''

class MainApp(MDApp):
    shoal = ObjectProperty()
    fish_num = ObjectProperty()
    dobs = ObjectProperty()
    strains = ObjectProperty()
    image = ObjectProperty()
    
    dialog =None
    
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        self.create_img_folder()
        
        return Builder.load_string(KV)
    
    def create_img_folder(self):
        """Create image folder"""
        image_folder = "./QRCodes"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            
    def create_qr(self):
        """Make qr code"""
        
        
        shoal_text = self.root.shoal.text
        fish_number_text = self.root.fish_num.text
        dob_text = self.root.dobs.text
        strain_text = self.root.strains.text
        
        img = qrcode.make({"id":shoal_text, 
                           "total_fish":fish_number_text, 
                           "DOB":dob_text, 
                           "strain":strain_text})
        
        """Save qr code in folder called the ID"""
        path = "./QRCodes//"+str(shoal_text)
        if not os.path.exists(path):
            os.makedirs(path)
        img_path = os.path.join(path, str(shoal_text)+".png")
        img.save(img_path)
        self.root.image.source = img_path
        self.show_alert_dialog()
            
    def reset_fields(self, instance):
        self.dialog.dismiss()
        self.root.shoal.text = ""
        self.root.fish_num.text = ""
        self.root.dobs.text = ""
        self.root.strains.text = ""
        self.root.image.source = ""
        
    
    def show_alert_dialog(self):
        btn1 = MDFlatButton(
                        text="Exit", text_color=self.theme_cls.primary_color
                    )
        btn2 = MDFlatButton(
                        text="Create Another", text_color=self.theme_cls.primary_color
                    )
        
        if not self.dialog:
            self.dialog = MDDialog(
                text="QRCode successful :)",
                buttons=[btn1,
                    btn2])
        self.dialog.open()
        btn2.bind(on_press = self.reset_fields)
        btn1.bind(on_press = self.close_app)

    def close_app(self, instance):
        self.dialog.dismiss()
        MDApp.get_running_app().stop()
        
MainApp().run()

