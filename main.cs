using System;

class Program
{
    unsafe static void Main()
    {
        int[] arr = { 1, 2, 3, 4 };

        fixed (int* p = arr) // pin array to prevent GC movement
        {
            for (int i = 0; i < arr.Length; i++)
                Console.WriteLine(*(p + i)); // pointer arithmetic
        }
    }
}
