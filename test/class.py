class Person:
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def introduce(self):
        return f"Hello, I am {self.name}. I am {self.age} years old."
    
    @classmethod
    def get_species(cls):
        return cls.species
    
    @staticmethod
    def is_adult(age):
        return age >= 18

print("Fisrt person: ")
person1 = Person("Alice", 23)
print(person1.introduce())
print(person1.get_species())
print("He is Adult." if person1.is_adult(person1.age) else "He is not Adult.")
print("\nAnother person: ")
person2 = Person("Sun", 10)
print(person2.introduce())
print(person2.get_species())
print("He is Adult." if person2.is_adult(person2.age) else "He is not Adult.")