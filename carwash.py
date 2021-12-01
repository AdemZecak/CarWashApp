import time
import mysql.connector
import random
import os 

#Wash with water and dry
#Wash with water, soap and dry
#Wash with water, soap, dry and polish

#Here is a happy path. A customer enters a shop, the employee enters which program to apply,
#and an eventual discount. The car wash process is simulated like each step writing to the console
#what is happening



#dio za konekciju sa bazom podataka
mydb = mysql.connector.connect (

    host = "localhost",
    user="root",
    password="root123456789",
    database="carwash"
)

mycursor = mydb.cursor()


print("-"*55)
print("Hello welcome to AntCarWash service!")
print("Thank you for using our services!")
print("-"*55)


#usluge koje se nude...važno je napomenuti da nakon svake treće posjete klijent ostvaruje popust

def services():

    print("")
    print("Services we offer: ")
    print("")
    print("1) Wash with water and dry for JUST 3$")
    print("2) Wash with water, soap and dry for JUST 6$")
    print("3) Wash with water, soap, dry and polish for JUST 9$.")
    print("")
    


#dio za registraciju

def registration():
    os.system("cls")
    print("-"*55)
    print("Welcome to registration section")
    print("-"*55)
    #predviđeno je da se klijent registruje i da ima svoju karticu preko koje će ostvarivati popust 
    ime = input("Enter your first name please: ")
    prezime = input("Enter your last name please:  ")
    #u listu će se dodati random brojevi od 1 do 99
    id_kartice_lista = []
    #prilikom registracije podrazumijeva se da klijent automatski ima svoju prvu posjetu i da će koristiti usluge
    broj_posjeta = 1

    #kroz for loop dodaju se brojevi u listu 'broj_posjeta' koji će činiti niz brojeva za id korisnika
    for i in range(0,4):
        id_kartice_lista.append(random.randint(1,99))

        id_kartice = ''.join(map(str,id_kartice_lista))
    
    #dio koji se veže za mysql bazu podataka i tabelu pod nazivom ant_car_wash gdje vodimo evidenciju o korisnicima
    customers = (ime,prezime,id_kartice,broj_posjeta)
    mycursor.execute("INSERT INTO ant_car_wash(ime,prezime,id_kartice,broj_posjeta) VALUES(%s,%s,%s,%s)",customers)
    mydb.commit()
    os.system("cls")

    print("-"*55)
    print(ime,prezime,"you are registred, thank you for choosing us.")
    print("-"*55)

    print("Your card ID:",id_kartice)
    print("Please remember your card ID, which you will need to get the discount.")


#korisnik koji je član treba samo priložiti svoj ID(u praksi zamišljeno kao očitavanje kartice)
#ukoliko nije član, treba se registrovati
member = input("Are you already our member? Yes(1) No(2): ")


if member == "1":
    #ukoliko je član, baza podataka to potvrđuje i može nastaviti sa korištenjem usluga
    mycursor.execute("SELECT id_kartice FROM ant_car_wash")
    values = mycursor.fetchall()

    id_kartice = input(str("Please enter your card ID: "))
    

    #for loop koristim da bi prošao kroz vrijednosti u koloni id_kartice
    for i in values:
        
        if (id_kartice,) in values:
            
            #izdvajam broj posjeta za tačno određenog korisnika da bi mogao provjeriti ostvaruje li popust
            sql = "SELECT broj_posjeta FROM ant_car_wash WHERE id_kartice = %s"
            mycursor.execute(sql,(id_kartice,))
            broj_posjeta = mycursor.fetchone()
            
            #nakon što je broj pronađen, dodaje se na istu vrijednost +1, i tako za svaku novu posjetu
            counter = broj_posjeta[0]

            broj_posjeta = counter + 1

            #podaci se updatuju u tabelu za tačno određenog korisnika
            posjete = (broj_posjeta,id_kartice)
            mycursor.execute("UPDATE ant_car_wash SET broj_posjeta = %s WHERE id_kartice = %s",posjete)
            mydb.commit()
            
            #discount sekcija
            #popust se daje na svaku treću posjetu
            
            sql = "SELECT broj_posjeta FROM ant_car_wash WHERE id_kartice = %s"
            mycursor.execute(sql,(id_kartice,))
            broj_posjeta = mycursor.fetchone()

            discount = broj_posjeta[0]

            if discount % 3 == 0: 
            
                print("-"*55)
                print("You have achieved discount!")
                print("-"*55)

                break
            else:
                pass

            break

        else:
            print("Wrong ID number, please try again.")
            exit()

elif member == "2":
    registration()


else: 
    os.system("cls")
    print("Something went wrong, please try again.")
    exit()



while True:

    
    services()
    #dio u kojem korisnik pristupa uslugama gdje na kraju korištenja saznaje da li ima popust ili ne
    customer = input("Please choose services you would like to use today 1/2/3: ")

    def first_option():
        
        print("")
        print("You have chosen our 'Wash with water and dry' option.")

        time.sleep(2)
        print("Car entering facility...")
        time.sleep(3)
        print("Car washing...")
        time.sleep(3)
        print("Car drying...")
        time.sleep(3)
        print("Finishing...")
        
        #if i else statement koristim da bih pristupio sekciji za popust ukoliko ga je korisnik ostvario
        #try except block koristim jer u slučaju registracije i prvog korištenja usluga, ne prolazim kroz discount varijablu, te na ovaj način izbjegavam grešku
                
        try: 
            if discount % 3 == 0:

                print("-"*55)
                print("You have achieved discount! Thank you for visiting us. Lucky Price: 1$.")
                print("-"*55)

            #ukoliko nema popust, usluge plaća fiksnim cijenama

            else:
                print("-"*55)
                print("Regular service price: 3$.")
                print("-"*55)
        except:
            print("-"*55)
            print("Regular service price: 3$.")
            print("-"*55)

        time.sleep(2)
        print("")
        print("Thank you for using AntCarWash services! Enjoy your ride!")
        print("")


    def second_option():

        print("")
        print("You have chosen our 'Wash with water,soap and dry' service.")
        time.sleep(2)
        print("Car entering facility...")
        time.sleep(3)
        print("Car washing...")
        time.sleep(3)
        print("Applying soap...")
        time.sleep(3)
        print("Car drying...")
        time.sleep(3)
        print("Finishing...")
        
        try:
            if discount % 3 == 0:

                print("-"*55)
                print("You have achieved discount! Thank you for visiting us. Lucky Price: 4$.")
                print("-"*55)

            #ukoliko nema popust, usluge plaća fiksnim cijenama
            else:
                print("-"*55)
                print("Regular service price: 6$.")
                print("-"*55)
        except:
            print("-"*55)
            print("Regular service price: 6$.")
            print("-"*55)

        time.sleep(2)
        print("")
        print("Thank you for using AntCarWash services! Enjoy your ride!")
        print("")


    def third_option():

        print("")
        print("You have chosen our 'Wash with water, soap, dry and polish' option.")
        time.sleep(2)
        print("Car entering facility...")

        time.sleep(3)
        print("Car washing...")
        time.sleep(3)
        print("Applying soap...")
        time.sleep(3)
        print("Car drying...")
        time.sleep(3)
        print("Car polishing...")
        print("Finishing...")
        
        try:

            if discount % 3 == 0:

                print("-"*55)
                print("You have achieved discount! Thank you for visiting us. Lucky Price: 7$.")
                print("-"*55)

            #ukoliko nema popust, usluge plaća fiksnim cijenama
            else:
                print("-"*55)
                print("Regular service price: 9$.")
                print("-"*55)
        except:
            print("-"*55)
            print("Regular service price: 9$.")
            print("-"*55)

        time.sleep(2)
        print("")
        print("Thank you for using AntCarWash services! Enjoy your ride!")
        print("")


    #sekcija koja aktivira jednu od tri ponuđene opcije 
    #funkcije sam koristio da bih dobio na preglednosti i da mi je sve podijeljeno u zasebne dijelove

    if customer == "1":
        
        first_option()
        break
        

    elif customer == "2":
        second_option()
        break
        

    elif customer == "3":
        third_option()
        break

    else: 
        print("Wrong input, please try again. ")

