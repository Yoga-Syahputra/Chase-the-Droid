#Inisiasi Tkinter dan random
import tkinter as tk
import random
from tkinter import messagebox
from collections import deque
from queue import Queue

#Inisiasi ukuran peta
CELL_SIZE = 20
MAZE_WIDTH = 25
MAZE_HEIGHT = 25

#Mendefinisikan peta
maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

#List untuk droid
droids = []

#Posisi permainan sebelum dimulai
game_paused = False

#Fungsi untuk menghasilkan peta
def generate_maze():
    stack = [(1, 1)]
    visited = set([(0, 0)])

    #Mengisi seluruh peta dengan dinding
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            maze[y][x] = 1

    while stack:
        x, y = stack[-1]

        # Temukan tetangga yang belum dikunjungi
        neighbors = []
        if x > 1 and (x - 2, y) not in visited:
            neighbors.append((x - 2, y))
        if x < MAZE_WIDTH - 2 and (x + 2, y) not in visited:
            neighbors.append((x + 2, y))
        if y > 1 and (x, y - 2) not in visited:
            neighbors.append((x, y - 2))
        if y < MAZE_HEIGHT - 2 and (x, y + 2) not in visited:
            neighbors.append((x, y + 2))

        if neighbors:
            # Pilih tetangga acak yang belum dikunjungi
            nx, ny = random.choice(neighbors)

            # Hubungkan tetangga dengan sel yang dikunjungi
            maze[(ny + y) // 2][(nx + x) // 2] = 0
            maze[ny][nx] = 0

            #Tandai tetangga sudah dikunjungi
            visited.add((nx, ny))

            #Tambahkan tetangga ke dalam stack
            stack.append((nx, ny))
        else:
            stack.pop()

    #Mengisi dinding di sekitar layar permainan
    for x in range(MAZE_WIDTH):
        maze[0][x] = 1
        maze[MAZE_HEIGHT - 1][x] = 1
    for y in range(MAZE_HEIGHT):
        maze[y][0] = 1
        maze[y][MAZE_WIDTH - 1] = 1

#Membuat peta
generate_maze()

#Inisiasi permainan
root = tk.Tk()
canvas = tk.Canvas(root, width=MAZE_WIDTH * CELL_SIZE, height=MAZE_HEIGHT * CELL_SIZE)
canvas.pack()

#Fungsi untuk menggambar peta
def draw_maze():
    # Menggambar dinding
    canvas.create_rectangle(0, 0, MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE, fill="yellow") #Menggambar dinding

    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0:
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black") #Menggambar jalur 

    canvas.create_oval(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE, (red_y + 1) * CELL_SIZE, fill="red", tags="red_droid")
    canvas.create_oval(green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE, (green_y + 1) * CELL_SIZE, fill="green", tags="green_droid")

#Inisiasi droid
red_x, red_y = 0, 0
green_x, green_y = MAZE_WIDTH - 1, MAZE_HEIGHT - 1

#Fungsi untuk menempatkan droid 
def place_droids():
    global green_x, green_y, red_x, red_y, droids

    #Menambahkan droid
    droids.append(green_droid)
    droids.append(red_droid)

    #Menghapus droid yang ada sebelumnya
    for droid in droids:
        canvas.delete(droid)

    droids = []  #Mengatur ulang list droid

    #Meletakkan droid hijau secara acak
    while True:
        green_x = random.randint(0, MAZE_WIDTH - 1)
        green_y = random.randint(0, MAZE_HEIGHT - 1)
        if maze[green_y][green_x] == 0:
            break

    #Meletakkan droid merah secara acak
    while True:
        red_x = random.randint(0, MAZE_WIDTH - 1)
        red_y = random.randint(0, MAZE_HEIGHT - 1)
        if maze[red_y][red_x] == 0 and (red_x, red_y) != (green_x, green_y):
            break

    #Menggambar droid pada canvas
    green_droid = canvas.create_oval(green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE,
                                     (green_y + 1) * CELL_SIZE, fill="green")
    red_droid = canvas.create_oval(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE,
                                   (red_y + 1) * CELL_SIZE, fill="red")
    
#Algoritma BFS - menemukan jalur terpendek
def find_shortest_path(start, end, visited):
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path + [current]

        x, y = current
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for neighbor in neighbors:
            if neighbor in visited:
                queue.append((neighbor, path + [current]))
                visited.remove(neighbor)

    return None

#Fungsi untuk menggerakkan droid merah
def move_red_droid():
    global red_x, red_y

    if red_x == green_x and red_y == green_y:
        canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2, MAZE_HEIGHT * CELL_SIZE // 2, text="SOLVED!", fill="red", font=("Arial", 24, "bold"), tags="solved_text")
        show_try_again_dialog()
        return

    queue = [(red_x, red_y)]
    visited = set([(red_x, red_y)])

    while queue:
        x, y = queue.pop(0)

        if (x, y) == (green_x, green_y):
            # Droid hijau ditemukan, tandai lokasinya
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="orange")
        else:
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black")

        # Pilih tetangga yang belum dikunjungi dan tidak berdinding
        neighbors = []
        if x > 0 and (x - 1, y) not in visited and maze[y][x - 1] != 1:
            neighbors.append((x - 1, y))
        if x < MAZE_WIDTH - 1 and (x + 1, y) not in visited and maze[y][x + 1] != 1:
            neighbors.append((x + 1, y))
        if y > 0 and (x, y - 1) not in visited and maze[y - 1][x] != 1:
            neighbors.append((x, y - 1))
        if y < MAZE_HEIGHT - 1 and (x, y + 1) not in visited and maze[y + 1][x] != 1:
            neighbors.append((x, y + 1))

        for nx, ny in neighbors:
            visited.add((nx, ny))
            queue.append((nx, ny))

        # Menemukan jalur yang menuju droid hijau, pilih jalur yang paling dekat
        if (green_x, green_y) in visited:
            path = find_shortest_path((red_x, red_y), (green_x, green_y), visited)
            if path:
                # Menggerakkan droid ke sel berikutnya dalam jalur terpendek
                next_x, next_y = path[1]
                canvas.create_rectangle(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE, (red_y + 1) * CELL_SIZE, fill="black")
                red_x, red_y = next_x, next_y
                canvas.create_oval(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE, (red_y + 1) * CELL_SIZE, fill="red")
                break

    if not game_paused:
        canvas.after(100, move_red_droid)

#Fungsi untuk menggerakkan droid hijau
def move_green_droid():
    global green_x, green_y

    if red_x == green_x and red_y == green_y:
        canvas.create_text(
            MAZE_WIDTH * CELL_SIZE // 2, MAZE_HEIGHT * CELL_SIZE // 2, text="SOLVED!", fill="red", font=("Arial", 24, "bold"), tags="solved_text")
        return

    visited = [[False] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    queue = Queue()
    queue.put((green_x, green_y))
    visited[green_y][green_x] = True
    found_path = False
    path = {}

    while not queue.empty():
        x, y = queue.get()

        if x == red_x and y == red_y:
            found_path = True
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and not visited[ny][nx] and maze[ny][nx] != 1
            ):
                queue.put((nx, ny))
                visited[ny][nx] = True
                path[(nx, ny)] = (x, y)

    if found_path:
        #Memilih jalur terpendek dari path
        shortest_path = []
        cx, cy = red_x, red_y

        while (cx, cy) != (green_x, green_y):
            shortest_path.append((cx, cy))
            cx, cy = path[(cx, cy)]

        shortest_path.reverse()
        farthest_distance = float('-inf')
        farthest_moves = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = green_x + dx, green_y + dy

            if (
                0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] != 1
                and (nx, ny) not in shortest_path
            ):
                distance = abs(nx - red_x) + abs(ny - red_y)

                if distance > farthest_distance:
                    farthest_distance = distance
                    farthest_moves = [(nx, ny)]
                elif distance == farthest_distance:
                    farthest_moves.append((nx, ny))

        if farthest_moves:
            #Memilih pergerakan yang paling jauh dari droid merah
            x, y = random.choice(farthest_moves)
            #Menghapus pergerakan terakhir dari jalur terpendek untuk menghindari putaran berulang
            shortest_path.pop()

            if (x, y) in shortest_path:
                # Menghapus pergerakan yang dipilih dari jalur terpendek
                index = shortest_path.index((x, y))
                shortest_path = shortest_path[:index]

        else:
            #Jika tidak ada pergerakan yang tersedia, putar balik dengan mengambil langkah sebelumnya dari jalur terpendek
            prev_x, prev_y = path[(green_x, green_y)]
            x, y = prev_x, prev_y

    else:
        #Jika tidak ada jalur yang ditemukan, putar balik dengan mengambil langkah sebelumnya dari jalur terpendek
        prev_x, prev_y = path[(green_x, green_y)]
        x, y = prev_x, prev_y

    # Menggerakkan droid hijau
    canvas.create_rectangle(
        green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE, (green_y + 1) * CELL_SIZE,
        fill="black"
    )
    green_x, green_y = x, y
    canvas.create_oval(
        green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE, (green_y + 1) * CELL_SIZE,
        fill="green"
    )

    # Menjadwalkan gerak selanjutnya
    if not game_paused:
        canvas.after(200, move_green_droid)

#Fungsi mengacak posisi droid
def randomize_droid_positions():
    global red_x, red_y, green_x, green_y

    while True:
        new_red_x, new_red_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
        new_green_x, new_green_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
        
        if maze[new_red_y][new_red_x] == 0 and maze[new_green_y][new_green_x] == 0 and (new_red_x, new_red_y) != (new_green_x, new_green_y):
            break

    #Hapus droid yang ada di posisi sebelumnya
    canvas.delete("red_droid")
    canvas.delete("green_droid")
    
    #Perbarui posisi droid merah
    red_x, red_y = new_red_x, new_red_y
    canvas.create_oval(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE, (red_y + 1) * CELL_SIZE, fill="red", tags="red_droid")
    
    #Perbarui posisi droid hijau
    green_x, green_y = new_green_x, new_green_y
    canvas.create_oval(green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE, (green_y + 1) * CELL_SIZE, fill="green", tags="green_droid")


#Variabel global untuk menghitung jumlah droid merah yang sudah ditambahkan
red_droid_count = 0

#Fungsi untuk menambah jumlah droid merah
def add_red_droid():
    global red_x, red_y, red_droid_count

    # Memeriksa apakah jumlah droid merah sudah mencapai batas maksimum
    if red_droid_count >= 5:
        messagebox.showinfo("Batas Droid Merah", "Jumlah droid yang ditambahkan sudah maksimum!")
        return

    # Membuat koordinat baru untuk penempatan droid merah
    new_red_x, new_red_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    while maze[new_red_y][new_red_x] == 1 or (new_red_x == green_x and new_red_y == green_y):
        new_red_x, new_red_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)

    # Menggambar droid merah baru
    red_droid = canvas.create_oval(new_red_x * CELL_SIZE, new_red_y * CELL_SIZE, (new_red_x + 1) * CELL_SIZE, (new_red_y + 1) * CELL_SIZE, fill="red")

    # Update variable global droid merah
    red_x, red_y = new_red_x, new_red_y

    # Menambahkan droid merah baru ke dalam list
    droids.append(red_droid)

    # Mengupdate jumlah droid merah yang sudah ditambahkan
    red_droid_count += 1

#Fungsi untuk menghapus droid merah
def remove_red_droid():
    global red_droid_count

    # Memeriksa apakah hanya ada satu droid merah tersisa
    if red_droid_count == 0:
        messagebox.showinfo("Jumlah Droid Merah", "Jumlah droid yang dikurangi sudah cukup!")
        return

    # Menghapus droid merah terakhir dari canvas dan list
    last_red_droid = droids.pop()
    canvas.delete(last_red_droid)

    # Mengurangi jumlah droid merah yang sudah ditambahkan
    red_droid_count -= 1

#Variabel untuk menyimpan status tombol terakhir dan keadaan tampilan
last_button = None
green_droid_visible = True
red_droid_visible = True

def show_red_droid_vision():
    global green_x, green_y, green_droid_visible, game_paused

    # Menyembunyikan droid hijau saat tidak terlihat
    if not green_droid_visible:
        canvas.delete("green_droid")

    # Tunjukkan visibilitas peta
    for i in range(-1, 2):
        for j in range(-1, 2):
            dx = green_x + i
            dy = green_y + j
            if 0 <= dx < MAZE_WIDTH and 0 <= dy < MAZE_HEIGHT:
                if maze[dy][dx] == 1:
                    canvas.create_rectangle(dx * CELL_SIZE + 1, dy * CELL_SIZE + 1, (dx + 1) * CELL_SIZE - 1,
                                            (dy + 1) * CELL_SIZE - 1, fill="yellow", outline="yellow")
                elif maze[dy][dx] == 0 and green_droid_visible:
                    canvas.create_rectangle(dx * CELL_SIZE, dy * CELL_SIZE, (dx + 1) * CELL_SIZE,
                                            (dy + 1) * CELL_SIZE, fill="black")

    # Menunjukkan droid merah
    red_x_pixel = red_x * CELL_SIZE
    red_y_pixel = red_y * CELL_SIZE
    canvas.create_oval(red_x_pixel, red_y_pixel, red_x_pixel + CELL_SIZE, red_y_pixel + CELL_SIZE, fill="red")

#Fungsi untuk menunjukkan pandangan droid hijau
def show_green_droid_vision():
    global green_x, green_y, last_button, green_droid_visible, red_droid_visible

    #Mengembalikan keadaan semula jika tombol yang sama ditekan kembali
    if last_button == "green":
        if not green_droid_visible:
            center_x = (green_x + 0.5) * CELL_SIZE
            center_y = (green_y + 0.5) * CELL_SIZE
            radius = CELL_SIZE * 2

            for i in range(MAZE_HEIGHT):
                for j in range(MAZE_WIDTH):
                    x = j * CELL_SIZE
                    y = i * CELL_SIZE
                    distance_squared = (x - center_x) ** 2 + (y - center_y) ** 2
                    if distance_squared <= radius ** 2:
                        if (i, j) == (green_y, green_x):
                            canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green", tags="green_droid")
                        elif maze[i][j] != 0:
                            if (i, j) == (green_y + 1, green_x) and maze[green_y + 1][green_x] != 1:  # Atas
                                canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE // 2, fill="yellow", outline="yellow")
                            elif (i, j) == (green_y - 1, green_x) and maze[green_y - 1][green_x] != 1:  # Bawah
                                canvas.create_rectangle(x, y + CELL_SIZE // 2, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
                            elif (i, j) == (green_y, green_x + 1) and maze[green_y][green_x + 1] != 1:  # Kanan
                                canvas.create_rectangle(x, y, x + CELL_SIZE // 2, y + CELL_SIZE, fill="yellow", outline="yellow")
                            elif (i, j) == (green_y, green_x - 1) and maze[green_y][green_x - 1] != 1:  # Kiri
                                canvas.create_rectangle(x + CELL_SIZE // 2, y, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
                            else:
                                canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
                    elif maze[i][j] != 0:
                        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="black", tags="green_droid")
            green_droid_visible = True
        else:
            for i in range(MAZE_HEIGHT):
                for j in range(MAZE_WIDTH):
                    if maze[i][j] != 0:
                        x = j * CELL_SIZE
                        y = i * CELL_SIZE
                        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="black", tags="green_droid")
            green_droid_visible = False
        return

    #Menunjukkan jarak pandang droid hijau
    center_x = (green_x + 0.5) * CELL_SIZE
    center_y = (green_y + 0.5) * CELL_SIZE
    radius = CELL_SIZE * 2

    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            distance_squared = (x - center_x) ** 2 + (y - center_y) ** 2
            if distance_squared <= radius ** 2:
                if (i, j) == (green_y, green_x):
                    canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green", tags="green_droid")
                elif maze[i][j] != 0:
                    if (i, j) == (green_y + 1, green_x) and maze[green_y + 1][green_x] != 1:  # Atas
                        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE // 2, fill="yellow", outline="yellow")
                    elif (i, j) == (green_y - 1, green_x) and maze[green_y - 1][green_x] != 1:  # Bawah
                        canvas.create_rectangle(x, y + CELL_SIZE // 2, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
                    elif (i, j) == (green_y, green_x + 1) and maze[green_y][green_x + 1] != 1:  # Kanan
                        canvas.create_rectangle(x, y, x + CELL_SIZE // 2, y + CELL_SIZE, fill="yellow", outline="yellow")
                    elif (i, j) == (green_y, green_x - 1) and maze[green_y][green_x - 1] != 1:  # Kiri
                        canvas.create_rectangle(x + CELL_SIZE // 2, y, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
                    else:
                        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="yellow")
            elif maze[i][j] != 0:
                canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="black", tags="green_droid")

    #Menampilkan droid merah
    if red_droid_visible:
        red_x_pixel = red_x * CELL_SIZE
        red_y_pixel = red_y * CELL_SIZE
        canvas.create_oval(red_x_pixel, red_y_pixel, red_x_pixel + CELL_SIZE, red_y_pixel + CELL_SIZE, fill="red", tags="red_droid")
        red_droid_visible = False

    #Menyimpan tombol terakhir yang ditekan
    last_button = "green"

#Fungsi untuk mengacak peta
def generate_new_maze():
    global maze
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    generate_maze()
    draw_maze()

#Fungsi untuk menginisiasi droid
def initialize_droids():
    global red_x, red_y, green_x, green_y
    red_x, red_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    green_x, green_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    
    while maze[red_y][red_x] == 1 or maze[green_y][green_x] == 1:
        red_x, red_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
        green_x, green_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    
    canvas.delete("red_droid")
    canvas.create_oval(red_x * CELL_SIZE, red_y * CELL_SIZE, (red_x + 1) * CELL_SIZE, (red_y + 1) * CELL_SIZE, fill="red", tags="red_droid")
    
    canvas.delete("green_droid")
    canvas.create_oval(green_x * CELL_SIZE, green_y * CELL_SIZE, (green_x + 1) * CELL_SIZE, (green_y + 1) * CELL_SIZE, fill="green", tags="green_droid")

#Fungsi untuk memulai permainan
def start_game():
    global game_paused
    game_paused = False
    move_red_droid()
    move_green_droid()

#Fungsi untuk menghentikan permainan
def stop_game():
    global game_paused
    game_paused = True

#Keluar dari permainan
def exit_game():
    root.destroy()

#Mengulang permainan
def reset_game():
    global green_x, green_y, red_x, red_y, droids
    canvas.delete("solved_text")

#Menunjukkan notifikasi setelah permainan selesai
def show_try_again_dialog():
    result = messagebox.askquestion("MESSAGE", "Try Again?")
    if result == "yes":
        reset_game()
    else:
        exit_game()

#Buat tombol
generate_maze_button = tk.Button(root, text="Generate Maze", command=generate_new_maze, bg="black", fg="white")
generate_maze_button.pack(side=tk.LEFT, padx=10, pady=10)

randomize_droid_position_button = tk.Button(root, text="Randomize Droid Position", command=randomize_droid_positions, bg="grey", fg="white")
randomize_droid_position_button.pack(side=tk.LEFT, padx=10, pady=10)

start_button = tk.Button(root, text="Start", command=start_game, bg="blue", fg="white")
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_game, bg="orange", fg="white")
stop_button.pack(side=tk.LEFT, padx=10, pady=10)

add_red_button = tk.Button(root, text="Add Red Droid", command=add_red_droid, bg="maroon", fg="white")
add_red_button.pack(side=tk.LEFT, padx=10, pady=10)

remove_red_button = tk.Button(root, text="Reduce Red Droid", command=remove_red_droid, bg="pink", fg="white")
remove_red_button.pack(side=tk.LEFT, padx=10, pady=10)

show_red_droid_vision_button = tk.Button(root, text="Red's POV", command=show_red_droid_vision, bg="red", fg="white")
show_red_droid_vision_button.pack(side=tk.LEFT, padx=10, pady=10)

show_green_droid_vision_button = tk.Button(root, text="Green's POV", command=show_green_droid_vision, bg="green", fg="white")
show_green_droid_vision_button.pack(side=tk.LEFT, padx=10, pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_game, bg="black", fg="white")
exit_button.pack(side=tk.LEFT, padx=10, pady=10)

#Inisiasi kembali
generate_new_maze()
initialize_droids()
root.configure(background="white")

#Memulai loop permainan
root.title("Chase the Droid!")
root.mainloop()
