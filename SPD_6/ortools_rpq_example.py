"""Ten skrypt przedstawia wykorzystanie metody CP w ramach biblioteki OR-Tools dla problemu RPQ.
Proszę uwzględnić, że kod nie jest zoptymalizowany - zależało mi, aby był maksymalnie czytelny, proszę ocenić czy się udało."""

class RPQ_Task:
    def __init__(self, task_number, r, p, q):
        """ Konstruktor klasy reprezentującej pojedyncze zadanie w ramach problemu RPQ,
         oprócz przechowywania danych o czasie przygotowania (r), czasie wykonania (p) oraz czasie dostarczenia (q) oraz numeru zadania (jako id)
          - klasa nie robi nic mądrego."""
        self.id: int = task_number
        self.r: int = r
        self.p: int = p
        self.q: int = q

class RPQ_Instance:
    """ Klasa przechowująca dane konkretniej instancji problemu - czyli wielu zadań jako (tasks) oraz liczby zadań (tasks_number)"""

    tasks: list[RPQ_Task] # lista wszystkich zadań, będą po kolei dla wygody
    tasks_number: int # liczba wszystkich zadań

    @staticmethod
    def load_from_file(file_path: str):
        """ Metoda wczytująca instancje z pliku - to zostawiam Państwu, na razie na sztywno dodana mała instancja."""
        instance = RPQ_Instance()
        instance.tasks_number = 4
        instance.tasks = [RPQ_Task(0, 0, 27, 78), RPQ_Task(1, 140, 7, 67), RPQ_Task(2, 14, 36, 54), RPQ_Task(3, 133, 76, 5)]
        return instance

    def get_r(self, task_number):
        """ Metoda dla czytelności - zwraca czas przygotowania dla zadania o podanym numerze."""
        return self.tasks[task_number].r

    def get_p(self, task_number): # analogicznie jak wyżej
        return self.tasks[task_number].p

    def get_q(self, task_number): # analogicznie jak wyżej
        return self.tasks[task_number].q



def solve_rpq_with_solver(instance: RPQ_Instance):
    """ W końcu funkcja rozwiązująca instancje problemu RPQ wykorzystując metodę CP z biblioteki or-tools"""
    from ortools.sat.python import cp_model # importujemy model CP z biblioteki or-tools

    model = cp_model.CpModel() # inicjalizacja modelu - przechowa nasze zmienne oraz ograniczenia naszego problemu

    # Model będzie operować na zmiennych całkowitoliczbowych - jakie zmienne? Czas rozpoczęcia, czas zakończenia, cmax...
    # Potrzebujemy określić zakres tych zmiennych - najmniej 0, bo nasz problem nie może mieć negatywnych czasów rozpoczęcia, zakończenia czy cmax.
    # Co z maksymalną wartością? Spróbujmy policzyć najbardziej pesymistyczny scenariusz (możliwie złą kolejność):
    # Dla tej złej kolejności zaczniemy od zadania, które ma największe r, później pozostałe zadania i na koniec zadanie o największym q
    # Gdybyśmy nie znali problemu, moglibyśmy po prostu dodać wszystkie czasy, byłby to gorszy zakres, więcej roboty dla solvera.

    max_r = 0
    max_q = 0
    sum_p = 0
    for task_number in range(instance.tasks_number): # iterujemy po wszystkich zadaniach:
        sum_p = sum_p + instance.get_p(task_number)
        max_r = max(max_r, instance.get_r(task_number))
        max_q = max(max_q, instance.get_q(task_number))

    variable_max_value = 1 + max_r + sum_p + max_q # dla pewności o jeden za dużo
    variable_min_value = 0 # nic nie jest ujemne w naszym wypadku

    # Zaraz będziemy inicjalizować zmienne wewnątrz modelu, aby łatwo się do nich odwoływać - tworzymy na razie puste listy:
    model_start_vars = [] # tutaj będą czasy rozpoczęć zadań
    model_ends_vars = [] # tutaj będą czasy zakończeń zadań
    model_interval_vars = [] # tutaj będą przechowywane zmienne odpowiedzialne za zmienne interwałowe

    # teraz inicjalizacja zmiennych wewnątrz modelu:
    # zaczniemy od pojedynczej zmiennej, która będzie przechowywać cmax - proszę zauważyć, że jest to zmienna tworzona
    # wewnątrz modelu i nie jest to typowy int - próba sprawdzenia, czy jest to pythonowy typ int zwróci fałsz:
    # aby stworzyć tą zmienną musimy podać zakres oraz nazwę zmiennej
    cmax_optimalization_objective = model.NewIntVar(variable_min_value, variable_max_value, 'cmax_makespan')
    print("type of cmax:", type(cmax_optimalization_objective), isinstance(cmax_optimalization_objective, int)) # można zakomentować bez żalu

    # więcej zmiennych: dla czasu rozpoczęcia, zakończenia i interwałów, ale dla każdego zdania więc korzystamy z pętli
    for task_number in range(instance.tasks_number):
        suffix = f"t:{task_number}" # do zmiennych należy dodawać nazwę - u nas będzie to po prostu numer zadania
        start_var = model.NewIntVar(variable_min_value, variable_max_value, 'start_' + suffix) # zmienna wewnątrz solvera odpowiedzialna za czas rozpoczęcia
        end_var = model.NewIntVar(variable_min_value, variable_max_value, 'end_' + suffix) # zmienna wewnątrz solvera odpowiedzialna za czas zakończenia
        # zmienna interwałowa "łączy" czas rozpoczęcia oraz czas zakonczenia - dodatkowo nasz wykonania zdania trwa dokładnie p:
        interval_var = model.NewIntervalVar(start_var, instance.get_p(task_number), end_var, 'interval_' + suffix) # zmienna interwałowa wewnątrz solvera odpowiedzialna za nie nakładanie się zadań

        # dodawanie zmiennych na listy pomocnicze:
        model_start_vars.append(start_var)
        model_ends_vars.append(end_var)
        model_interval_vars.append(interval_var)

    # Pora na dodanie ograniczeń - zacznimy od najtrudniejszego: nasze zadania nie mogą się na siebie "nakładać na siebie",
    # czyli jedyna maszyna w problemie RPQ może pracować na raz tylko nad jednym zadaniem.
    # W ramach CP jest to ograniczenie łatwe do dodania:
    model.AddNoOverlap(model_interval_vars)
    # Gdybyśmy mieli więcej maszyn to musielibyśmy trochę bardziej pokombinować, ale ponieważ w RPQ jest jedna maszyna to
    # dodajemy wszystkie interwały. W wypadku wielomaszynowym tylko interwały z tej samej maszyny nie mogły się nakładać.

    # Pora teraz na ograniczenie związane z czasem rozpoczęcia - tutaj sytuacja jest jasna: start zadania jest możliwy dopiero po upływie czasu rozpoczęcia (r)
    for task_number in range(instance.tasks_number):
        model.Add(model_start_vars[task_number] >= instance.get_r(task_number)) # dodajemy do modelu ograniczenie w postaci nierówność

    # Zostało nam ograniczenie związane z czasem dostarczenia...
    # My zawrzemy je w ramach obliczenia cmaxa - proszę zwrócić uwagę, że cmax to największy czas dostarczenia ze wszystkich zadań
    # łatwo to przedstawić jako odpowiednią nierówność - cmax musi być większy/równy od czasu dostarczenia dla każdego zadania
    for task_number in range(instance.tasks_number):
        model.Add(cmax_optimalization_objective >= model_ends_vars[task_number] + instance.get_q(task_number))

    # Pora dodać do modelu informacje czego właściwie szukamy - chcemy zminimalizować cmax więc:
    model.Minimize(cmax_optimalization_objective)

    # Inicjalizujemy solver, który spróbuje znaleźć rozwiązanie w ramach naszego modelu:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0 # dodatkowo ograniczmy czas wykonywania obliczeń do maksymalnie 5 min

    # Wszystkie ograniczenia dodane! pora odpalić solver!
    status = solver.Solve(model) # solver zwróci status, ale jako typ wyliczeniowy, więc troche nieczytelnie dla nas

    if (status is not cp_model.OPTIMAL): # sprawdzamy status, aby określić czy solver znalazł rozwiązanie optymalne
        status_readable = "not optimal solution :("
    else:
        status_readable = "optimum found!"

    # Oprócz cmaxa przydałoby się odczytać kolejność wykonywania zadań - dla RPQ będzie to łatwe.
    # Wystarczy, że sprawdzimy czasy rozpoczęć (lub zakończeń) dla poszczególnych zadań:
    # Tworzymy listę z parami: (numer zadania, czas rozpoczęcia), sortujemy po tej drugiej wartości.
    pi_order = []
    for task_number in range(instance.tasks_number):
        pi_order.append((task_number, solver.Value(model_start_vars[task_number])))
    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order] # modyfikujemy naszą listę, aby przechowywać tylko numer zadań, bez czasów rozpoczęć

    return solver.ObjectiveValue(), pi_order, status_readable # zwracamy cmax, kolejność wykonywania zadań oraz informacje czy znaleźliśmy optimum



if __name__ == '__main__':
    # ten if będzie spełniony, tylko jeśli odpalimy bezpośrednio ten skrypt, nie jeśli zaimportujemy ten plik z innego pliku

    # tutaj przydałaby się jeszcze pętla, aby odpalać metodę dla każdej instancji z foleru...
    test_instance = RPQ_Instance.load_from_file("scieżka do pliku - tak by było gdyby wczytywanie działało")
    cmax, pi_order, status = solve_rpq_with_solver(test_instance)
    print(f"Script ended, cmax: {cmax}, order: {pi_order}\nis optimal? {status}")


# Na koniec jeszcze jedna uwaga: w wypadku błędów proszę pierwsze co sprawdzić poprawność instalacji biblioteki oraz czy
# w ramach własnej implementacji dla innych problemów:
# wszystkie nierówności są reprezentowane jako zmienne całkowitoliczbowe (koniecznie int).