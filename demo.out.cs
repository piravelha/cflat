using CFlat;

namespace Demo
{
    public class Program
    {
        public class Box<T>
        {
            public T Value { get; init; }
            public Box(T _Value)
            {
                Value = _Value;
            }
        }
        
        public static void Main()
        {
            Box<int> box = new(10);
            println(box.Value);
        }
    }
}