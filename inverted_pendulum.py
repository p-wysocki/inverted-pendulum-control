import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as ani
import numpy as np
from numpy import sin, cos, arctan2
from itertools import cycle
from sys import argv, exit
import baza_regul, defuzyfikacja

class InvertedPendulum():
    '''Inicjalizacja stałych:
    M - masa wózka
    m - masa kulki
    l - długość ramienia wahadła

    Warunków początkowych:
    x0 - początkowe położenie wózka
    dx0 - początkowa prędkość wózka
    theta0 - początkowe położenie wahadla
    dtheta0 - początkowa prędkość wahadła

    Zakłócenia zewnętrznego:
    dis_cyc - zmienna odpowiada za to, czy zakłócenie jest zapętlone
    disruption - wartości zakłócenia w kolejnych chwilach czasowych

    Parametry planszy/obrazka:
    iw, ih - szerokość i wysokość obrazka
    x_max - maksymalna współrzędna pozioma (oś x jest symetryczna, więc minimalna wynosi -x_max)
    h_min - minialna współrzędna pionowa
    h_max - maksymalna współrzędna pionowa

    Powyższe dane są pobierane z pliku jeśli zmienna f_name nie jest pusta'''
    def __init__(self, M=10, m=5, l=50, x0=0, theta0=0, dx0=0, dtheta0=0, dis_cyc=True, disruption=[0], iw=1000, ih=500, x_max=100, h_min=0, h_max=100, f_name=None):
        if f_name:
            with open(f_name) as f_handle:
                lines = f_handle.readlines()
                init_cond = lines[0].split(' ')
                self.M, self.m, self.l, self.x0, self.theta0, self.dx0, self.dtheta0 = [float(el) for el in init_cond[:7]]
                self.image_w, self.image_h, self.x_max, self.h_min, self.h_max = [int(el) for el in init_cond[-5:]]
                if lines[1]:
                    self.disruption = cycle([float(el) for el in lines[2].split(' ')])
                else:
                    self.disruption = iter([float(el) for el in lines[2].split(' ')])
        else:
            self.M, self.m, self.l, self.x0, self.theta0, self.dx0, self.dtheta0 = M, m, l, x0, theta0, dx0, dtheta0
            self.image_w, self.image_h, self.x_max, self.h_min, self.h_max = iw, ih, x_max, h_min, h_max
            if dis_cyc:
                self.disruption = cycle(disruption)
            else:
                self.disruption = iter(disruption)

    # Funkcja odpowiedzialna za wyłączenie programu, gdy zostanie zamknięte okno z rysunkami
    def handle_close(self, evt):
        exit(0)

    # Inicjalizacja obrazka
    def init_image(self, x, theta):
        dpi = 100
        self.fig, ax = plt.subplots(figsize=(self.image_w/dpi, self.image_h/dpi), dpi=dpi)
        plt.autoscale(False)
        plt.xticks(range(-self.x_max, self.x_max+1, int(self.x_max/10)))
        plt.yticks(range(self.h_min, self.h_max+1, int(self.h_max/10)))
        self.hor = 10
        self.c_w = 16
        self.c_h = 8
        r = 4
        self.cart = patches.Rectangle((x-self.c_w/2, self.hor-self.c_h/2), self.c_w, self.c_h,linewidth=1, edgecolor='blue',facecolor='blue', zorder=2)
        self.blob = patches.Circle((x-self.l*sin(theta), self.hor+self.l*cos(theta)), r ,linewidth=1, edgecolor='red',facecolor='red', zorder=3)
        self.guide = patches.Rectangle((-self.x_max, self.hor-1), 2*self.x_max, 2, edgecolor='black',facecolor='black', zorder=0)
        self.arm = patches.Rectangle((x+cos(theta), self.hor+sin(theta)), self.l, 2, 180*theta/np.pi+90, edgecolor='brown', facecolor='brown', zorder=1)
        ax.add_patch(self.cart)
        ax.add_patch(self.blob)
        ax.add_patch(self.guide)
        ax.add_patch(self.arm)

    #    Aktualizacja położenia wózka, ramienia i wahadła
    def update_image(self, data):
        x, theta = data[0], data[1]
        self.cart.set_x(x-self.c_w/2)
        self.blob.set_center((x-self.l*sin(theta), self.hor+self.l*cos(theta)))
        self.arm.angle = theta*180/np.pi+90
        self.arm.set_xy((x+cos(theta), self.hor+sin(theta)))
        return self.cart, self.blob, self.arm,

    # Rozwiązanie równań mechaniki wahadła
    def solve_equation(self, x, theta, dx, dtheta, F):
        l, m, M = self.l, self.m, self.M
        g = 9.81
        a11 = M+m
        a12 = -m*l*cos(theta)
        b1 = F-m*l*dtheta**2*sin(theta)
        a21 = -cos(theta)
        a22 = l
        b2 = g*sin(theta)
        a = np.array([[a11, a12], [a21, a22]])
        b = np.array([b1, b2])
        sol = np.linalg.solve(a, b)
        return sol[0], sol[1]

    # Scałkowanie numeryczne przyśpieszenia, żeby uzyskać pozostałe parametry układu
    def count_state_params(self, x, theta, dx, dtheta, F, dt=0.001):
        ddx, ddtheta = self.solve_equation(x, theta, dx, dtheta, F)
        dx += ddx*dt
        x += dx*dt
        dtheta += ddtheta*dt
        theta += dtheta*dt
        theta = arctan2(sin(theta), cos(theta))
        return x, theta, dx, dtheta

    # Funkcja generująca kolejne dane symulacji
    def generate_data(self):
        x = self.x0
        theta = self.theta0
        dx = self.dx0
        dtheta = self.dtheta0
        while True:
            for i in range(self.frameskip+1):
                dis=next(self.disruption, 0)
                control = self.fuzzy_control(x, theta, dx, dtheta)
                F = dis+control
                x, theta, dx, dtheta = self.count_state_params(x, theta, dx, dtheta, F)
                if not self.sandbox:
                    if x < -self.x_max or x > self.x_max or np.abs(theta) > np.pi/3:
                        exit(1)
            yield x, theta

    # Uruchomienie symulacji
    # Zmienna sandbox mówi o tym, czy symulacja ma zostać przerwana w przypadku nieudanego sterowania -
    # - to znaczy takiego, które pozwoliło na zbyt duże wychylenia iksa lub na zbyt poziomo położenie wahadła
    def run(self, sandbox, frameskip=200):
        self.init_image(self.x0, self.theta0)
        self.sandbox = sandbox
        self.frameskip = frameskip
        a = ani.FuncAnimation(self.fig, self.update_image, self.generate_data, interval=1)
        plt.show()
        
    # Regulator rozmyty, który trzeba zaimplementować
    def fuzzy_control(self, x, theta, dx, dtheta):
        push_cart_left, push_cart_right = baza_regul.get_rules_outputs(x, theta, dx, dtheta)
        force = defuzyfikacja.get_cart_force(push_cart_left, push_cart_right)
        return force

if __name__ == '__main__':
        if len(argv)>1:
            ip = InvertedPendulum(f_name=argv[1])
        else:
            ip = InvertedPendulum(x0=90, dx0=0, theta0=0, dtheta0=0.1, ih=800, iw=1000, h_min=-80, h_max=80)
        ip.run(sandbox=True)
