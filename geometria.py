{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib widget\n",
    "# Narzędzie jest oparte o kilka zewnętrznych bibliotek, które potrzebujemy najpierw zaimportować.\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.collections as mcoll\n",
    "import matplotlib.colors as mcolors\n",
    "from matplotlib.widgets import Button\n",
    "import json as js\n",
    "\n",
    "# Parametr określający jak blisko (w odsetku całego widocznego zakresu) punktu początkowego \n",
    "# wielokąta musimy kliknąć, aby go zamknąć.\n",
    "TOLERANCE = 0.15\n",
    "\n",
    "def dist(point1, point2):\n",
    "    return np.sqrt(np.power(point1[0] - point2[0], 2) + np.power(point1[1] - point2[1], 2))\n",
    "\n",
    "# Klasa ta trzyma obecny stan wykresu oraz posiada metody, które mają zostać wykonane\n",
    "# po naciśnięciu przycisków.\n",
    "class _Button_callback(object):\n",
    "    def __init__(self, scenes):\n",
    "        self.i = 0\n",
    "        self.scenes = scenes\n",
    "        self.adding_points = False\n",
    "        self.added_points = []\n",
    "        self.adding_lines = False\n",
    "        self.added_lines = []\n",
    "        self.adding_rects = False\n",
    "        self.added_rects = []\n",
    "\n",
    "    def set_axes(self, ax):\n",
    "        self.ax = ax\n",
    "        \n",
    "    # Metoda ta obsługuje logikę przejścia do następnej sceny.\n",
    "    def next(self, event):\n",
    "        self.i = (self.i + 1) % len(self.scenes)\n",
    "        self.draw(autoscaling = True)\n",
    "\n",
    "    # Metoda ta obsługuje logikę powrotu do poprzedniej sceny.\n",
    "    def prev(self, event):\n",
    "        self.i = (self.i - 1) % len(self.scenes)\n",
    "        self.draw(autoscaling = True)\n",
    "        \n",
    "    # Metoda ta aktywuje funkcję rysowania punktów wyłączając równocześnie rysowanie \n",
    "    # odcinków i wielokątów.\n",
    "    def add_point(self, event):\n",
    "        self.adding_points = not self.adding_points\n",
    "        self.new_line_point = None\n",
    "        if self.adding_points:\n",
    "            self.adding_lines = False\n",
    "            self.adding_rects = False\n",
    "            self.added_points.append(PointsCollection([]))\n",
    "            \n",
    "    # Metoda ta aktywuje funkcję rysowania odcinków wyłączając równocześnie\n",
    "    # rysowanie punktów i wielokątów.     \n",
    "    def add_line(self, event):   \n",
    "        self.adding_lines = not self.adding_lines\n",
    "        self.new_line_point = None\n",
    "        if self.adding_lines:\n",
    "            self.adding_points = False\n",
    "            self.adding_rects = False\n",
    "            self.added_lines.append(LinesCollection([]))\n",
    "\n",
    "    # Metoda ta aktywuje funkcję rysowania wielokątów wyłączając równocześnie\n",
    "    # rysowanie punktów i odcinków.\n",
    "    def add_rect(self, event):\n",
    "        self.adding_rects = not self.adding_rects\n",
    "        self.new_line_point = None\n",
    "        if self.adding_rects:\n",
    "            self.adding_points = False\n",
    "            self.adding_lines = False\n",
    "            self.new_rect()\n",
    "    \n",
    "    def new_rect(self):\n",
    "        self.added_rects.append(LinesCollection([]))\n",
    "        self.rect_points = []\n",
    "        \n",
    "    # Metoda odpowiedzialna za właściwą logikę rysowania nowych elementów. W\n",
    "    # zależności od włączonego trybu dodaje nowe punkty, początek, koniec odcinka\n",
    "    # lub poszczególne wierzchołki wielokąta. Istnieje ciekawa logika sprawdzania\n",
    "    # czy dany punkt jest domykający dla danego wielokąta. Polega ona na tym, że\n",
    "    # sprawdzamy czy odległość nowego punktu od początkowego jest większa od\n",
    "    # średniej długości zakresu pomnożonej razy parametr TOLERANCE.   \n",
    "    def on_click(self, event):\n",
    "        if event.inaxes != self.ax:\n",
    "            return\n",
    "        new_point = (event.xdata, event.ydata)\n",
    "        if self.adding_points:\n",
    "            self.added_points[-1].add_points([new_point])\n",
    "            self.draw(autoscaling = False)\n",
    "        elif self.adding_lines:\n",
    "            if self.new_line_point is not None:\n",
    "                self.added_lines[-1].add([self.new_line_point, new_point])\n",
    "                self.new_line_point = None\n",
    "                self.draw(autoscaling = False)\n",
    "            else:\n",
    "                self.new_line_point = new_point\n",
    "        elif self.adding_rects:\n",
    "            if len(self.rect_points) == 0:\n",
    "                self.rect_points.append(new_point)\n",
    "            elif len(self.rect_points) == 1:\n",
    "                self.added_rects[-1].add([self.rect_points[-1], new_point])\n",
    "                self.rect_points.append(new_point)\n",
    "                self.draw(autoscaling = False)\n",
    "            elif len(self.rect_points) > 1:\n",
    "                if dist(self.rect_points[0], new_point) < (np.mean([self.ax.get_xlim(), self.ax.get_ylim()])*TOLERANCE):\n",
    "                    self.added_rects[-1].add([self.rect_points[-1], self.rect_points[0]])\n",
    "                    self.new_rect()\n",
    "                else:    \n",
    "                    self.added_rects[-1].add([self.rect_points[-1], new_point])\n",
    "                    self.rect_points.append(new_point)\n",
    "                self.draw(autoscaling = False)\n",
    "    \n",
    "    # Metoda odpowiedzialna za narysowanie całego wykresu. Warto zauważyć,\n",
    "    # że zaczyna się ona od wyczyszczenia jego wcześniejszego stanu. Istnieje w\n",
    "    # niej nietrywialna logika zarządzania zakresem wykresu, tak żeby, w zależności\n",
    "    # od ustawionego parametru autoscaling, uniknąć sytuacji, kiedy dodawanie\n",
    "    # nowych punktów przy brzegu obecnie widzianego zakresu powoduje niekorzystne\n",
    "    # przeskalowanie.\n",
    "    def draw(self, autoscaling = True):\n",
    "        if not autoscaling:\n",
    "            xlim = self.ax.get_xlim()\n",
    "            ylim = self.ax.get_ylim()\n",
    "        self.ax.clear()\n",
    "        for collection in (self.scenes[self.i].points + self.added_points):\n",
    "            if len(collection.points) > 0:\n",
    "                self.ax.scatter(*zip(*(np.array(collection.points))), **collection.kwargs)\n",
    "        for collection in (self.scenes[self.i].lines + self.added_lines + self.added_rects):\n",
    "            self.ax.add_collection(collection.get_collection())\n",
    "        self.ax.autoscale(autoscaling)\n",
    "        if not autoscaling:\n",
    "            self.ax.set_xlim(xlim)\n",
    "            self.ax.set_ylim(ylim)\n",
    "        plt.draw()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Klasa Scene odpowiada za przechowywanie elementów, które mają być\n",
    "# wyświetlane równocześnie. Konkretnie jest to lista PointsCollection i\n",
    "# LinesCollection.\n",
    "class Scene:\n",
    "    def __init__(self, points=[], lines=[]):\n",
    "        self.points=points\n",
    "        self.lines=lines\n",
    "\n",
    "# Klasa PointsCollection gromadzi w sobie punkty jednego typu, a więc takie,\n",
    "# które zostaną narysowane w takim samym kolorze i stylu. W konstruktorze\n",
    "# przyjmuje listę punktów rozumianych jako pary współrzędnych (x, y). Parametr\n",
    "# kwargs jest przekazywany do wywołania funkcji z biblioteki MatPlotLib przez\n",
    "# co użytkownik może podawać wszystkie parametry tam zaproponowane.        \n",
    "class PointsCollection:\n",
    "    def __init__(self, points, **kwargs):\n",
    "        self.points = points\n",
    "        self.kwargs = kwargs\n",
    "    \n",
    "    def add_points(self, points):\n",
    "        self.points = self.points + points\n",
    "\n",
    "# Klasa LinesCollection podobnie jak jej punktowy odpowiednik gromadzi\n",
    "# odcinki tego samego typu. Tworząc ją należy podać listę linii, gdzie każda\n",
    "# z nich jest dwuelementową listą punktów – par (x, y). Parametr kwargs jest\n",
    "# przekazywany do wywołania funkcji z biblioteki MatPlotLib przez co użytkownik\n",
    "# może podawać wszystkie parametry tam zaproponowane.\n",
    "class LinesCollection:\n",
    "    def __init__(self, lines, **kwargs):\n",
    "        self.lines = lines\n",
    "        self.kwargs = kwargs\n",
    "        \n",
    "    def add(self, line):\n",
    "        self.lines.append(line)\n",
    "        \n",
    "    def get_collection(self):\n",
    "        return mcoll.LineCollection(self.lines, **self.kwargs)\n",
    "\n",
    "# Klasa Plot jest najważniejszą klasą w całym programie, ponieważ agreguje\n",
    "# wszystkie przygotowane sceny, odpowiada za stworzenie wykresu i przechowuje\n",
    "# referencje na przyciski, dzięki czemu nie będą one skasowane podczas tzw.\n",
    "# garbage collectingu.\n",
    "class Plot:\n",
    "    def __init__(self, scenes = [Scene()], points = [], lines = [], json = None):\n",
    "        if json is None:\n",
    "            self.scenes = scenes\n",
    "            if points or lines:\n",
    "                self.scenes[0].points = points\n",
    "                self.scenes[0].lines = lines\n",
    "        else:\n",
    "            self.scenes = [Scene([PointsCollection(pointsCol) for pointsCol in scene[\"points\"]], \n",
    "                                 [LinesCollection(linesCol) for linesCol in scene[\"lines\"]]) \n",
    "                           for scene in js.loads(json)]\n",
    "    \n",
    "    # Ta metoda ma szczególne znaczenie, ponieważ konfiguruje przyciski i\n",
    "    # wykonuje tym samym dość skomplikowaną logikę. Zauważmy, że konfigurując każdy\n",
    "    # przycisk podajemy referencję na metodę obiektu _Button_callback, która\n",
    "    # zostanie wykonana w momencie naciśnięcia.\n",
    "    def __configure_buttons(self):\n",
    "        plt.subplots_adjust(bottom=0.2)\n",
    "        ax_prev = plt.axes([0.6, 0.05, 0.15, 0.075])\n",
    "        ax_next = plt.axes([0.76, 0.05, 0.15, 0.075])\n",
    "        ax_add_point = plt.axes([0.44, 0.05, 0.15, 0.075])\n",
    "        ax_add_line = plt.axes([0.28, 0.05, 0.15, 0.075])\n",
    "        ax_add_rect = plt.axes([0.12, 0.05, 0.15, 0.075])\n",
    "        b_next = Button(ax_next, 'Następny')\n",
    "        b_next.on_clicked(self.callback.next)\n",
    "        b_prev = Button(ax_prev, 'Poprzedni')\n",
    "        b_prev.on_clicked(self.callback.prev)\n",
    "        b_add_point = Button(ax_add_point, 'Dodaj punkt')\n",
    "        b_add_point.on_clicked(self.callback.add_point)\n",
    "        b_add_line = Button(ax_add_line, 'Dodaj linię')\n",
    "        b_add_line.on_clicked(self.callback.add_line)\n",
    "        b_add_rect = Button(ax_add_rect, 'Dodaj figurę')\n",
    "        b_add_rect.on_clicked(self.callback.add_rect)\n",
    "        return [b_prev, b_next, b_add_point, b_add_line, b_add_rect]\n",
    "    \n",
    "    def add_scene(self, scene):\n",
    "        self.scenes.append(scene)\n",
    "    \n",
    "    def add_scenes(self, scenes):\n",
    "        self.scenes = self.scenes + scenes\n",
    "\n",
    "    # Metoda toJson() odpowiada za zapisanie stanu obiektu do ciągu znaków w\n",
    "    # formacie JSON.\n",
    "    def toJson(self):\n",
    "        return js.dumps([{\"points\": [np.array(pointCol.points).tolist() for pointCol in scene.points], \n",
    "                          \"lines\":[linesCol.lines for linesCol in scene.lines]} \n",
    "                         for scene in self.scenes])    \n",
    "    \n",
    "    # Metoda ta zwraca punkty dodane w trakcie rysowania.\n",
    "    def get_added_points(self):\n",
    "        if self.callback:\n",
    "            return self.callback.added_points\n",
    "        else:\n",
    "            return None\n",
    "    \n",
    "    # Metoda ta zwraca odcinki dodane w trakcie rysowania.\n",
    "    def get_added_lines(self):\n",
    "        if self.callback:\n",
    "            return self.callback.added_lines\n",
    "        else:\n",
    "            return None\n",
    "        \n",
    "    # Metoda ta zwraca wielokąty dodane w trakcie rysowania.\n",
    "    def get_added_figure(self):\n",
    "        if self.callback:\n",
    "            return self.callback.added_rects\n",
    "        else:\n",
    "            return None\n",
    "    \n",
    "    # Metoda ta zwraca punkty, odcinki i wielokąty dodane w trakcie rysowania\n",
    "    # jako scenę.\n",
    "    def get_added_elements(self):\n",
    "        if self.callback:\n",
    "            return Scene(self.callback.added_points, self.callback.added_lines+self.callback.added_rects)\n",
    "        else:\n",
    "            return None\n",
    "    \n",
    "    # Główna metoda inicjalizująca wyświetlanie wykresu.\n",
    "    def draw(self):\n",
    "        plt.close()\n",
    "        fig = plt.figure()\n",
    "        self.callback = _Button_callback(self.scenes)\n",
    "        self.widgets = self.__configure_buttons()\n",
    "        ax = plt.axes(autoscale_on = False)\n",
    "        self.callback.set_axes(ax)\n",
    "        fig.canvas.mpl_connect('button_press_event', self.callback.on_click)\n",
    "        plt.show()\n",
    "        self.callback.draw()\n",
    "        "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0]"
  },
  "orig_nbformat": 4,
  "vscode": {
   "interpreter": {
    "hash": "916dbcbb3f70747c44a77c7bcd40155683ae19c65e1c03b4aa3499c5328201f1"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
