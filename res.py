import random
def is_prime(n):
    if n <= 1:
        return True
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return True
    return False
def Game(x):
    print("Enter for start Game")
    n=input()
    over=1
    n=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    Exp=0
    coin=0
    nev=0
    combo=0
    comboMax=0
    if x==1:
        Hp=3
        while over:
            ans=1
            nev=0
            for i in range(2):
                a=(random.randrange(0,3,1))
                ans=ans*n[a]
            print(ans)
            ans1=list(map(int, input().split()))
            kk=1
            for i in ans1:
                kk=kk*i
                if is_prime(i):
                    nev=1
            if kk==ans and nev==0:
                coin+=1
                Exp+=1
                combo+=1
                print("combo",combo)
            else:
                Hp-=1
                comboMax=max(combo,comboMax)
                combo=0
                print(f"""Hp:{Hp}/3""", end=":")
                if nev:
                    print("There are non-prime numbers")
                else:
                    print("ans wrong")
                if Hp==0:
                    over=False
    elif x==2:
        Hp=3
        while over:
            ans=1
            nev=0
            for i in range(3):
                a=(random.randrange(0,5,1))
                ans=ans*n[a]
            print(ans)
            ans1=list(map(int, input().split()))
            kk=1
            for i in ans1:
                kk=kk*i
                if is_prime(i):
                    nev=1
            if kk==ans and nev==0:
                coin+=3
                Exp+=5
                combo+=1
                print("combo",combo)
            else:
                Hp-=1
                comboMax=max(combo,comboMax)
                combo=0
                print(f"""Hp:{Hp}/3""", end=":")
                if nev:
                    print("There are non-prime numbers")
                else:
                    print("ans wrong")
                if Hp==0:
                    over=False
    elif x==3:
        Hp=3
        while over:
            ans=1
            nev=0
            for i in range(3):
                a=(random.randrange(0,7,1))
                ans=ans*n[a]
            print(ans)
            ans1=list(map(int, input().split()))
            kk=1
            for i in ans1:
                kk=kk*i
                if is_prime(i):
                    nev=1
            if kk==ans and nev==0:
                coin+=10
                Exp+=10
                combo+=1
                print("combo",combo)
            else:
                Hp-=1
                comboMax=max(combo,comboMax)
                combo=0
                print(f"""Hp:{Hp}/3""", end=":")
                if nev:
                    print("There are non-prime numbers")
                else:
                    print("ans wrong")
                if Hp==0:
                    over=False
    elif x==4:
        Hp=2
        while over:
            ans=1
            nev=0
            for i in range(4):
                a=(random.randrange(0,10,1))
                ans=ans*n[a]
            print(ans)
            ans1=list(map(int, input().split()))
            kk=1
            for i in ans1:
                kk=kk*i
                if is_prime(i):
                    nev=1
            if kk==ans and nev==0:
                coin+=30
                Exp+=20
                combo+=1
                print("combo",combo)
            else:
                Hp-=1
                comboMax=max(combo,comboMax)
                combo=0
                print(f"""Hp:{Hp}/2""", end=":")
                if nev:
                    print("There are non-prime numbers")
                else:
                    print("ans wrong")
                if Hp==0:
                    over=False
    elif x==5:
        Hp=1
        while over:
            ans=1
            nev=0
            for i in range(5):
                a=(random.randrange(0,24,1))
                ans=ans*n[a]
            print(ans)
            ans1=list(map(int, input().split()))
            kk=1
            for i in ans1:
                kk=kk*i
                if is_prime(i):
                    nev=1
            if kk==ans and nev==0:
                coin+=50
                Exp+=40
                combo+=1
                print("combo",combo)
            else:
                Hp-=1
                comboMax=max(combo,comboMax)
                combo=0
                print(f"""Hp:{Hp}/1""", end=":")
                if nev:
                    print("There are non-prime numbers")
                else:
                    print("ans wrong")
                if Hp==0:
                    over=False
    print("""Game Over
""","Exp",Exp,"coin",coin,"combo",comboMax,"""
Enter for Exit""")
    n=input()
def main():
    print("""
prime game
(1)  Play
(2)  Shop         (開發中)
(3)  Skin         (開發中)
(4)  Achievements (開發中)
(5)  Item         (開發中)
(6)  Option       (開發中)
(88) Exit game""")
def core_menu():
    print("""
(1) Baby   [Exp:1    Coin:1  ] Hp:3/3
(2) Eazy   [Exp:5    Coin:3  ] Hp:3/3
(3) Normal [Exp:10   Coin:10 ] Hp:3/3
(4) Hard   [Exp:20   Coin:30 ] Hp:2/2
(5) Asia   [Exp:40   Coin:50 ] Hp:1/1
(0) Exit
""")
page="main"
while True:
    try:
        if page=="main":
            main()
            Tin=input()
            if not Tin:
                continue
            the=int(Tin)
            if the == 1:
                page="core"
            elif the==88:
                print("Bye")
                break
            else:
                print("Nope")
        elif page=="core":
            core_menu()
            Tin=input()
            if not Tin:
                continue
            the = int(Tin)
            if the == 0:
                page = "main"
            elif the in [1, 2, 3, 4, 5]:
                Game(the)
                page = "main"
            else:
                print("Nope")
    except ValueError:
        print(end="")
    except Exception as e:
        print(f"error:{e}")
        break