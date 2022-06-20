using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection.Emit;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace MIW06
{
    class Program
    {

        static double Funkcja(double x1, double x2)
        {
            return Math.Sin(x1 * 0.05) + Math.Sin(x2 * 0.05) + 0.4 * Math.Sin(x1 * 0.15) * Math.Sin(x2 * 0.15);
        }

        static void Mutacja(int[,] potomne, Random rnd, int k){
            for(int j = k; j<potomne.GetLength(0)-1; j++)
                {
                    int mutacja = rnd.Next(0, potomne.GetLength(1));
                    if (potomne[j, mutacja] == 0)
                        potomne[j, mutacja] = 1;
                    else
                        potomne[j, mutacja] = 0;
                }
        }

        static void Krzyzowanie(int[,] potomne, Random rnd, int r1, int r2)
        {
            int[,] potomek1 = new int[1,potomne.GetLength(1)];
            int[,] potomek2 = new int[1,potomne.GetLength(1)];

            int linia = rnd.Next(0, potomne.GetLength(1)-2);
            for (int i=0; i<=linia;i++)
            {
                potomek1[0,i] = potomne[r1,i];
                potomek2[0, i] = potomne[r2, i];
            }
            for (int i = linia+1 ; i < potomne.GetLength(1)-1; i++)
            {
                potomek1[0, i] = potomne[r2, i];
                potomek2[0, i] = potomne[r1, i];
            }
            for(int i=0; i< potomne.GetLength(1); i++)
            {
                potomne[r1, i] = potomek1[0, i];
                potomne[r2, i] = potomek2[0, i];
            }
        }

        static void SelekcjaTurniejowa(int[,] potomne,int[,] osobniki, int RozTur, Random rnd, double[] funkcja_przystosowania)
        {
            for (int k = 0; k < potomne.GetLength(0) - 1; k++)
            {
                int[] turniej = new int[RozTur];
                for (int r = 0; r < RozTur; r++)
                    turniej[r] = rnd.Next(0, potomne.GetLength(0));
                double najlepszy = funkcja_przystosowania[turniej[0]];
                int wiersz = turniej[0];
                for (int r = 0; r < RozTur; r++)
                {
                    if (najlepszy < funkcja_przystosowania[turniej[r]])
                    {
                        najlepszy = funkcja_przystosowania[turniej[r]];
                        wiersz = turniej[r];
                    }
                }
                for (int j = 0; j < potomne.GetLength(1); j++)
                    potomne[k, j] = osobniki[wiersz, j];
            }
        }

        static int Dekodowanie(int[,] chromosomy, int LBnCh, int l, int[] dekodowanie)
        {
            for (l = 0; l < chromosomy.GetLength(0); l++)
            {
                int tmp = 0;
                for (int m = 0; m < LBnCh; m++)
                {
                    if (chromosomy[l, m] == dekodowanie[m])
                        tmp++;
                    else
                    {
                        tmp = 0;
                        break;
                    }
                }
                if (tmp == LBnCh)
                    break;
            }
            return l;
        }

        static void Chromosomy(int[,] chromosomy, double wiersze, int LBnCh)
        {
            for (int i = 0; i < wiersze; i++)
            {
                short j = Convert.ToInt16(LBnCh - 1);
                while (j >= 0)
                {
                    chromosomy[i, LBnCh - j - 1] = (i >> j) & 1;
                    j--;
                }
            }
        }

        static double Funkcja2(double pa, double pb, double pc, double x)
        {
            return pa * Math.Sin(pb * x + pc);
        }

    static void Main(string[] args)
        {
            //ZADANIE 1
            Console.WriteLine("ZADANIE 1");
            Console.WriteLine();

            Random rnd = new Random();
            double przedzial_od = 0; //min przedziału
            double przedzial_do = 100; //max przedziału
            int LBnCh = 3; //liczba chromosomów
            int LO = 9; //liczba osobników
            double przedzial = przedzial_do - przedzial_od; //różnica przedziałów
            double wiersze = Math.Pow(2, LBnCh); //liczba wierszy 
            double wartosc_przedzialu = przedzial / (wiersze - 1); //wartości dla parametrów
            double wartosci = przedzial_od; //pierwszy parametr
            int iteracje = 20;
            int RozTur = 2; //Rozmiar Turnieju

            int[,] chromosomy = new int[(int)wiersze, LBnCh];
            double[] parametry = new double[(int)wiersze];
            double[] funkcja_przystosowania = new double[LO];
            double[] funkcja_potomna = new double[LO];
            int[,] osobniki = new int[LO, LBnCh*2];
            int[,] potomne = new int[LO, LBnCh * 2];

            //wartości chromosomów
            Chromosomy(chromosomy, wiersze, LBnCh);

            //wartości parametrów modelu
            for(int i=0; i < parametry.Length; i++)
            {
                parametry[i] = wartosci;
                wartosci += wartosc_przedzialu;
            }

            //wylosowane osobników długości LBnCh*2 oraz policzona funkcja przystosowania dla nowych osobników
            for(int i = 0; i < LO; i++)
            {
                int wiersz1 = rnd.Next(0,(int)wiersze);
                int wiersz2 = rnd.Next(0, 8);
                int j, k;
                for (j = 0; j < LBnCh; j++)
                    osobniki[i, j] = chromosomy[wiersz1,j];
                for(k=0; k< LBnCh; k++)
                    osobniki[i, LBnCh + k] = chromosomy[wiersz2, k];
                funkcja_przystosowania[i] = Funkcja(parametry[wiersz1], parametry[wiersz2]);
            }

            for(int x=0; x< osobniki.GetLength(0); x++)
                {
                    for(int y=0; y<osobniki.GetLength(1); y++){
                        Console.Write(osobniki[x, y]);
                    }
                    Console.WriteLine();
                }
        

            //algorytm genetyczny
            for(int i=0; i < iteracje; i++)
            {
                //wyszukanie najlepszego rodzica
                double rodzic = funkcja_przystosowania[0];
                int WR = 0;
                for (int a = 1; a < LO; a++)
                {
                    if (rodzic < funkcja_przystosowania[a])
                    {
                        rodzic = funkcja_przystosowania[a];
                        WR = a;
                    }
                }

                //selekcja turniejowa i wyznaczenie osobników potomnych
                SelekcjaTurniejowa(potomne, osobniki, RozTur, rnd, funkcja_przystosowania);


                //mutacja jednopunktowa
                Mutacja(potomne, rnd, 0);

                //dodanie najlepszego rodzica do potomnych "hot deck"
                for (int k = 0; k < LBnCh * 2; k++)
                    potomne[LO-1,k] = osobniki[WR, k];
                funkcja_potomna[LO - 1] = funkcja_przystosowania[WR];

                //wyliczanie nowej wartości funkcji przystosowania dla nowych osobników z puli
                for(int j = 0; j < LO-1; j++)
                {
                    double x1, x2;
                    int k,l = 0;
                    int[] dekodowanie = new int[LBnCh];
                    for (k = 0; k < LBnCh; k++)
                        dekodowanie[k] = potomne[j, k];
                    l = Dekodowanie(chromosomy, LBnCh, 0, dekodowanie);
                    x1 = parametry[l];
                    for (k=LBnCh; k < LBnCh*2; k++)
                        dekodowanie[k-LBnCh] = potomne[j, k];
                    l = Dekodowanie(chromosomy, LBnCh, 0, dekodowanie);
                    x2 = parametry[l];
                    funkcja_potomna[j] = Funkcja(x1, x2);    
                }

                //wypisanie najlepszej wartości funkcji przystosowania oraz średnią wartość funkcji
                // Console.WriteLine("Iteracja "+(i+1)+":");
                // Console.WriteLine("Najlepsza wartość funkcji przystosowania (największa): "+funkcja_potomna.Max());
                // Console.WriteLine("Średnia wartość funkcji przystosowania: "+funkcja_potomna.Average());
                // Console.WriteLine();
                osobniki = potomne;
                funkcja_przystosowania = funkcja_potomna;
            }
            
            Console.ReadKey();
        }
    }
}

