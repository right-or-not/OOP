import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class ArrayListExample {
    public static void main(String[] args) {
        // 1. 创建 ArrayList
        ArrayList<String> fruits = new ArrayList<>();
        
        // 2. 添加元素
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Orange");
        fruits.add("Mango");
        
        System.out.println("初始列表: " + fruits);
        
        // 3. 在指定位置插入元素
        fruits.add(1, "Grapes");
        System.out.println("插入葡萄后: " + fruits);
        
        // 4. 获取元素
        String firstFruit = fruits.get(0);
        System.out.println("第一个水果: " + firstFruit);
        
        // 5. 修改元素
        fruits.set(2, "Cherry");
        System.out.println("修改后: " + fruits);
        
        // 6. 删除元素
        fruits.remove("Banana"); // 按对象删除
        System.out.println("删除香蕉后: " + fruits);
        
        fruits.remove(0); // 按索引删除
        System.out.println("删除第一个元素后: " + fruits);
        
        // 7. 获取列表大小
        System.out.println("列表大小: " + fruits.size());
        
        // 8. 检查是否包含元素
        System.out.println("是否包含苹果: " + fruits.contains("Apple"));
        System.out.println("是否包含芒果: " + fruits.contains("Mango"));
        
        // 9. 检查列表是否为空
        System.out.println("列表是否为空: " + fruits.isEmpty());
        
        // 10. 获取元素索引
        System.out.println("芒果的索引: " + fruits.indexOf("Mango"));
        
        // 11. 清空列表
        fruits.clear();
        System.out.println("清空后列表: " + fruits);
        System.out.println("清空后是否为空: " + fruits.isEmpty());
        
        // 重新添加一些元素
        fruits.add("Watermelon");
        fruits.add("Pineapple");
        fruits.add("Strawberry");
        fruits.add("Blueberry");
        
        // 12. 遍历 ArrayList - 方法1: for循环
        System.out.println("\n使用for循环遍历:");
        for (int i = 0; i < fruits.size(); i++) {
            System.out.println("索引 " + i + ": " + fruits.get(i));
        }
        
        // 13. 遍历 ArrayList - 方法2: 增强for循环
        System.out.println("\n使用增强for循环遍历:");
        for (String fruit : fruits) {
            System.out.println(fruit);
        }
        
        // 14. 遍历 ArrayList - 方法3: 使用迭代器
        System.out.println("\n使用迭代器遍历:");
        Iterator<String> iterator = fruits.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
        
        // 15. 遍历 ArrayList - 方法4: 使用forEach方法 (Java 8+)
        System.out.println("\n使用forEach方法遍历:");
        fruits.forEach(fruit -> System.out.println(fruit));
        
        // 16. 使用Lambda表达式和方法引用
        System.out.println("\n使用方法引用遍历:");
        fruits.forEach(System.out::println);
        
        // 17. 将ArrayList转换为数组
        String[] fruitArray = fruits.toArray(new String[0]);
        System.out.println("\n转换为数组: " + Arrays.toString(fruitArray));
        
        // 18. 使用其他集合初始化ArrayList
        List<String> moreFruits = Arrays.asList("Peach", "Pear", "Plum");
        ArrayList<String> combinedList = new ArrayList<>(fruits);
        combinedList.addAll(moreFruits);
        System.out.println("\n合并后的列表: " + combinedList);
        
        // 19. 子列表操作
        List<String> subList = combinedList.subList(2, 5);
        System.out.println("子列表(2-5): " + subList);
        
        // 20. 排序ArrayList
        System.out.println("\n排序前: " + combinedList);
        combinedList.sort(String::compareToIgnoreCase);
        System.out.println("排序后: " + combinedList);
        
        // 21. 使用自定义比较器排序
        combinedList.sort((s1, s2) -> s2.compareTo(s1)); // 反向排序
        System.out.println("反向排序: " + combinedList);
        
        // 22. 使用ArrayList存储自定义对象
        ArrayList<Person> people = new ArrayList<>();
        people.add(new Person("Alice", 25));
        people.add(new Person("Bob", 30));
        people.add(new Person("Charlie", 22));
        
        System.out.println("\n人员列表:");
        people.forEach(person -> 
            System.out.println(person.getName() + " - " + person.getAge() + "岁"));
        
        // 按年龄排序
        people.sort((p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
        System.out.println("\n按年龄排序后:");
        people.forEach(person -> 
            System.out.println(person.getName() + " - " + person.getAge() + "岁"));
    }
    
    // 自定义类示例
    static class Person {
        private String name;
        private int age;
        
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }
        
        public String getName() {
            return name;
        }
        
        public int getAge() {
            return age;
        }
    }
}