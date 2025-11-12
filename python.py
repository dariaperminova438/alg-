import numpy as np
import random
from collections import deque

class EmployeeScheduling:
    def __init__(self, num_employees, num_days, work_days_per_employee, max_consecutive_days_off):
        self.num_employees = num_employees
        self.num_days = num_days
        self.work_days_per_employee = work_days_per_employee
        self.max_consecutive_days_off = max_consecutive_days_off
        
        self.schedule = np.zeros((num_employees, num_days), dtype=int)
        self.initialize_schedule()
        
        self.tabu_list = deque(maxlen=10)
        
    def initialize_schedule(self):
        for employee in range(self.num_employees):
            work_days = random.sample(range(self.num_days), self.work_days_per_employee)
            for day in work_days:
                self.schedule[employee][day] = 1
    
    def calculate_cost(self, schedule):
        cost = 0
        
        for employee in range(self.num_employees):
            consecutive_off = 0
            for day in range(self.num_days):
                if schedule[employee][day] == 0:
                    consecutive_off += 1
                    if consecutive_off > self.max_consecutive_days_off:
                        cost += 10
                else:
                    consecutive_off = 0
        
        daily_workload = np.sum(schedule, axis=0)
        ideal_workload = self.num_employees * self.work_days_per_employee / self.num_days
        for day in range(self.num_days):
            cost += abs(daily_workload[day] - ideal_workload) * 2
        
        for employee in range(self.num_employees):
            actual_work_days = np.sum(schedule[employee])
            if actual_work_days != self.work_days_per_employee:
                cost += abs(actual_work_days - self.work_days_per_employee) * 20
        
        return cost
    
    def get_neighbors(self, schedule):
        neighbors = []
        
        for employee in range(self.num_employees):
            for day1 in range(self.num_days):
                for day2 in range(self.num_days):
                    if day1 != day2 and schedule[employee][day1] != schedule[employee][day2]:
                        new_schedule = schedule.copy()
                        new_schedule[employee][day1], new_schedule[employee][day2] = \
                            new_schedule[employee][day2], new_schedule[employee][day1]
                        
                        move = (employee, day1, day2)
                        if move not in self.tabu_list:
                            neighbors.append((new_schedule, move))
        
        return neighbors
    
    def tabu_search(self, max_iterations=1000):
        current_schedule = self.schedule.copy()
        current_cost = self.calculate_cost(current_schedule)
        
        best_schedule = current_schedule.copy()
        best_cost = current_cost
        
        for iteration in range(max_iterations):
            neighbors = self.get_neighbors(current_schedule)
            
            if not neighbors:
                break
            
            best_neighbor_cost = float('inf')
            best_neighbor = None
            best_move = None
            
            for neighbor, move in neighbors:
                neighbor_cost = self.calculate_cost(neighbor)
                
                if neighbor_cost < best_neighbor_cost or neighbor_cost < best_cost:
                    best_neighbor_cost = neighbor_cost
                    best_neighbor = neighbor
                    best_move = move
            
            if best_neighbor is None:
                break
            
            current_schedule = best_neighbor
            current_cost = best_neighbor_cost
            
            self.tabu_list.append(best_move)
            
            if current_cost < best_cost:
                best_schedule = current_schedule.copy()
                best_cost = current_cost
        
        self.schedule = best_schedule
        return best_schedule, best_cost
    
    def print_schedule(self):
        print("\nФИНАЛЬНОЕ РАСПИСАНИЕ")
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        
        print("     " + " ".join(f"{day:>3}" for day in days[:self.num_days]))
        
        for i in range(self.num_employees):
            row = [f"{'В' if self.schedule[i][j] == 0 else 'Р':>3}" for j in range(self.num_days)]
            print(f"Сотр {i+1}: " + " ".join(row))
        
        print("\nР - рабочий день, В - выходной")
        
        print(f"\nСТАТИСТИКА:")
        print(f"Общая стоимость расписания: {self.calculate_cost(self.schedule):.2f}")
        
        violations = 0
        for i in range(self.num_employees):
            consecutive_off = 0
            for j in range(self.num_days):
                if self.schedule[i][j] == 0:
                    consecutive_off += 1
                    if consecutive_off > self.max_consecutive_days_off:
                        violations += 1
                else:
                    consecutive_off = 0
        
        print(f"Нарушения последовательных выходных: {violations}")
        
        daily_load = np.sum(self.schedule, axis=0)
        print(f"Нагрузка по дням: {daily_load}")
        print(f"Идеальная нагрузка: {self.num_employees * self.work_days_per_employee / self.num_days:.1f}")

def main():
    print("ТАБУ ПОИСК ДЛЯ ЗАДАЧИ ПЛАНИРОВАНИЯ РАБОТНИКОВ")
    
    # Ввод данных
    num_employees = int(input("Количество работников: "))
    num_days = int(input("Количество дней в периоде: "))
    work_days_per_employee = int(input("Количество рабочих дней на одного работника: "))
    max_consecutive_days_off = int(input("Максимальное количество выходных подряд: "))
    max_iterations = int(input("Максимальное количество итераций алгоритма: "))
    
    # Запуск алгоритма
    print("\nЗапуск табу поиска...")
    scheduler = EmployeeScheduling(num_employees, num_days, work_days_per_employee, max_consecutive_days_off)
    final_schedule, final_cost = scheduler.tabu_search(max_iterations)
    
    # Вывод результатов
    scheduler.print_schedule()
    
    # Оценка качества
    print(f"\nОЦЕНКА КАЧЕСТВА РАСПИСАНИЯ:")
    cost = scheduler.calculate_cost(final_schedule)
    
    if cost == 0:
        print("Расписание идеально удовлетворяет всем ограничениям")
    elif cost < 10:
        print("Расписание хорошего качества с минимальными нарушениями")
    elif cost < 30:
        print("Расписание приемлемого качества")
    else:
        print("Расписание требует улучшения")

if __name__ == "__main__":
    main()
