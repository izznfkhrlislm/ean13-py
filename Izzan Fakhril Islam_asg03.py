########################################################################
#       Programming Assignment 3 (Foundations of Programming 1)	       #
#       Name: Izzan Fakhril Islam                                      #
#       Student ID: 1606875806                                         #
#       Class: F                                                       #
########################################################################

#Importing the functions needed to run this app
from tkinter import *
import tkinter.messagebox #Tkinter message box (error, info, etc)
class Barcode:
	def __init__(self):
		master = Tk()
		#Lock the window so it can't be resized
		master.minsize(width = 350, height = 400)
		master.maxsize(width = 350, height = 400)
		#Assign a title for the app
		master.title("EAN-13 [by Izzan Fakhril Islam]")
		print("Selamat datang di program GUI saya! Selamat menikmati :) jangan lupa kritik dan saran yah.")
		
		#Creating dictionaries containing the ABC/LGR code
		A = {0 : "0001101", 1 : "0011001", 2 : "0010011", 3 : "0111101", 4 : "0100011", 5 : "0110001", 6 : "0101111", 7 : "0111011", 8 : "0110111", 9 : "0001011"}
		B = {0 : "0100111", 1 : "0110011", 2 : "0011011", 3 : "0100001", 4 : "0011101", 5 : "0111001", 6 : "0000101", 7 : "0010001", 8 : "0001001", 9 : "0010111"}
		C = {0 : "1110010", 1 : "1100110", 2 : "1101100", 3 : "1000010", 4 : "1011100", 5 : "1001110", 6 : "1010000", 7 : "1000100", 8 : "1001000", 9 : "1110100"}
		self.ld = C
		#Creating dictionaries containing the ABC/LGR code pattern for each input digit
		self.fd = {0 : (A,A,A,A,A,A), 1 : (A,A,B,A,B,B), 2 : (A,A,B,B,A,B), 3 : (A,A,B,B,B,A), 4 : (A,B,A,A,B,B), 5 : (A,B,B,A,A,B), 6 : (A,B,B,B,A,A), 7 : (A,B,A,B,A,B), 8 : (A,B,A,B,B,A), 9 : (A,B,B,A,B,A)}		
		
		self.message = Label(master, text = "Save Barcode to PostScript file [eg: EAN13.eps]:", fg = "black")
		self.input1 = StringVar()
		self.entername = Entry(master, width = 25, bg = "white", textvariable = self.input1) #creating input for the file name
		self.message2 = Label(master, text = "Enter code (first 12 decimal digits):", fg = "black")
		self.input2 = StringVar()
		self.entervalue = Entry(master, width = 25, bg = "white", textvariable = self.input2) #creating input for the first 12 digit barcode number
		
		self.canvas = Canvas(master, width = 300, height = 300, bg = "white") #creating the Canvas for drawing the barcode
		
		#Binding enter key (<Return>) event to the specified functions
		self.entername.bind("<Return>", self.save)
		self.entervalue.bind("<Return>", self.clear, add = "+")
		self.entervalue.bind("<Return>", self.checksum, add = "+")
		self.entervalue.bind("<Return>", self.inti, add = "+")
		self.entervalue.bind("<Return>", self.draw, add = "+")
		
		self.message.pack()
		self.entername.pack()
		self.message2.pack()
		self.entervalue.pack()
		self.canvas.pack()
		
		master.mainloop()
		
	def checksum(self, event): #Creating checksum (13th digit) from the first 12 barcode digits
		try:
			value = self.entervalue.get()
			if len(value) > 12 or len(value) < 12 and len(value) != 0 and value.isdigit():
				tkinter.messagebox.showerror("Invalid number of digits", "Only 12 digits of number are allowed.")
			elif len(value) == 0:
				tkinter.messagebox.showerror("Empty Input", "Please enter an input")
			else:
				tin = [int(i) for i in value]
				odd = 0
				even = 0
				for k in range(1,12,2):
					odd += tin[k]
				for j in range(0,12,2):
					even += tin[j]
				checksum = odd*3 + even
				self.checkdigit = checksum % 10
				if self.checkdigit != 0:
					self.checkdigit = 10 - self.checkdigit
				self.res = value+str(self.checkdigit)
			if value.isdigit() == False and len(value) > 0:
				tkinter.messagebox.showerror("Invalid Input", "Please enter a number!")
		except ValueError:
			tkinter.messagebox.showerror("Invalid Input", "Please enter a number!")
		except IndexError:
			pass
		except AttributeError:
			pass
		
	def inti(self,event): #Creating binary patterns from the 13-digit barcode number
		try:
			angka = self.res
			daftar = [int(z) for z in angka]
			firstDigit = self.fd[daftar[0]]
			self.firstSix = ''
			self.nextSix = ''
			for i in range(6):
				ght = firstDigit[i][daftar[i+1]]
				self.firstSix = self.firstSix + ght
			for i in range(6,12):
				fga = self.ld[daftar[i+1]]
				self.nextSix = self.nextSix + fga
			self.hasil = self.firstSix+self.nextSix
			self.start = [1,0,1] #list consisting binary patterns of first and last guard bar
			self.middle = [0,1,0,1,0] #list consisting binary patterns of middle guard bar
		except ValueError:
			tkinter.messagebox.showerror("Invalid input", "Please enter a number!")
		except IndexError:
			pass
		except AttributeError:
			pass
	
	def draw(self,event): #draw black and white lines from the barcode binary patterns
		try:
			self.canvas.create_text(150, 30 , font = ("Arial", 17), text = "EAN-13 Barcode", fill = "black")
			x = 60
			for num in self.start: #First guard bar
				if num == 1:
					self.canvas.create_line(x,60,x,220, fill = "black", width = 2)
					x += 2
				else:
					self.canvas.create_line(x,60,x,220, fill = "white", width = 2)
					x += 2
			jadi = [int(obj) for obj in self.firstSix]
			for num in jadi: #First six numbers of barcode (digit 2-7)
				if num == 1:
					self.canvas.create_line(x,60,x,200, fill = "black", width = 2)
					x += 2
				else:
					self.canvas.create_line(x,60,x,200, fill = "white", width = 2)
					x += 2
			for num in self.middle: #Middle guard number
				if num == 1:
					self.canvas.create_line(x,60,x,220, fill = "black", width = 2)
					x += 2
				else:
					self.canvas.create_line(x,60,x,220, fill = "white", width = 2)
					x += 2
			akhir = [int(obj) for obj in self.nextSix]
			for num in akhir: #Second six numbers of barcode (digit 7-12)
				if num == 1:
					self.canvas.create_line(x,60,x,200, fill = "black", width = 2)
					x += 2
				else:
					self.canvas.create_line(x,60,x,200, fill = "white", width = 2)
					x += 2
			for num in self.start: #Last guard number
				if num == 1:
					self.canvas.create_line(x,60,x,220, fill = "black", width = 2)
					x += 2
				else:
					self.canvas.create_line(x,60,x,220, fill = "white", width = 2)
					x += 2
			digitPrint = self.res
			self.canvas.create_text(50, 220, font = ("Arial", 17), text = digitPrint[0])
			self.canvas.create_text(110, 220, font = ("Arial", 17), text = digitPrint[1:7])
			self.canvas.create_text(200, 220, font = ("Arial", 17), text = digitPrint[7:])
			self.canvas.create_text(150, 270, font = ("Arial", 17), text = "Check Digit: "+digitPrint[-1], fill = "black")	
		except AttributeError:
			pass
	
	def clear(self,event): #Resetting the canvas to the default when a new entry is applied
		self.canvas.delete("all")
		
	def save(self,event): #Saving the file in .eps document format
		nama = self.entername.get()
		if len(nama) == 0:
			tkinter.messagebox.showerror("Enter a name", "Please assign a name for your file.")
		elif ".eps" not in nama:
			tkinter.messagebox.showerror("Enter your extension", "Please enter your extension (.eps)")
		else:
			self.canvas.postscript(file = nama)
			tkinter.messagebox.showinfo("Save Successful", "Your file has been saved in your root directory of this app") 
													
if __name__ == "__main__":
	Barcode()				
