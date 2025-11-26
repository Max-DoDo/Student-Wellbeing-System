
'''
This class is the init class for the programme. Its UI object and database object are created in this class.
This class should not be subclassed.
'''
from entity.person import Person
class App:
    
    def __init__(self):
        
        self.main()

    def main(self) -> None:

        self.test()
    
    def test(self) -> None:
        
        person = Person(id = 10000, name="Max",gender="Male")
        print(person)




if __name__ == "__main__":
    app = App()

