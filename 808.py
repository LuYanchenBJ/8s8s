import tkinter as tk
import random
import time


# 设定的参数
colors = ['red', 'blue', 'green']  # 修改颜色选项为红色、蓝色、绿色
linestyles = [(),(10, 5)]  # 增加线型选项
widths = [3,9]  # 增加宽度选项

correct_answers = []
total_correct = 0
total_questions = 0
current_question = 0  # 添加当前问题的指示器
remaining_time = 300  # 剩余时间，单位秒
start_time = time.time()  # 游戏开始时的时间

def draw_triangle(canvas, x, y, color, linestyle, width):
  points = [x, y, x + 100, y, x + 50, y + 87]
  for i in range(3):
    if linestyle[i]:
      canvas.create_line(points[i*2], points[i*2+1], points[(i*2+2)%6], points[(i*2+3)%6], fill=color[i], dash=linestyle[i], width=width[i])
    else:
      canvas.create_line(points[i*2], points[i*2+1], points[(i*2+2)%6], points[(i*2+3)%6], fill=color[i], width=width[i])

def check_answer(index, value):
  global total_correct, total_questions, current_question
  if current_question == index:  # 确保用户只能回答当前问题
    if correct_answers[index] == value:
      total_correct += 1
    total_questions += 1
    current_question += 1
    if current_question == 8:  # 如果所有题目都被回答了，则生成新的题目
      generate_triangles()
    update_buttons_state()

def update_buttons_state():
  for i in range(8):
    btns_correct[i].config(state=tk.NORMAL if i == current_question else tk.DISABLED)
    btns_wrong[i].config(state=tk.NORMAL if i == current_question else tk.DISABLED)

def update_timer():
  global remaining_time, start_time
  elapsed_time = time.time() - start_time  # 计算已过去的时间



  
  remaining_time = max(0, 300 - int(elapsed_time))  # 计算剩余时间
  

  
  timer_label.config(text=f"剩余时间：{remaining_time}秒")
  if remaining_time > 0:
    root.after(1000, update_timer)
  else:
    end_game()

def generate_triangles():
  global correct_answers, current_question, start_time
  canvas.delete('all')

  # 生成例题三角形的属性
  random.shuffle(colors)
  example_color = colors[:3]
  example_linestyle = [random.choice(linestyles) for _ in range(3)]
  example_width = [random.choice(widths) for _ in range(3)]

  draw_triangle(canvas, 50, 100, example_color, example_linestyle, example_width)

  correct_answers = []
  current_question = 0  # 重置当前问题的指示器
  btns_correct.clear()  # 重置正确按钮的列表
  btns_wrong.clear()  # 重置错误按钮的列表

  for i in range(8):  # 生成八个三角形
    x = 200 + i * 150
    # 修改答案是正确的概率为0.5
    if random.random() < 0.5:
      color,linestyle,width =example_color, example_linestyle, example_width
      correct_answers.append(1)
    else:
      a=random.randint(1,3)
      if a==1:
        color,linestyle=example_color, example_linestyle
        width = [random.choice(widths) for _ in range(3)]
      elif a==2:
        linestyle,width = example_linestyle, example_width
        random.shuffle(colors)
        color = colors[:3]
      elif a==3:
        color,width=example_color,example_width
        linestyle = [random.choice(linestyles) for _ in range(3)]  
      if color==example_color and linestyle==example_linestyle and width==example_width:
        correct_answers.append(1)
      else:  
        correct_answers.append(0)
        

    draw_triangle(canvas, x, 100, color, linestyle, width)

    btn_correct = tk.Button(root, text="✓", command=lambda i=i: check_answer(i, 1))
    btn_correct.config(state=tk.NORMAL if i == current_question else tk.DISABLED)  # 只有当前问题的按钮是激活的
    canvas.create_window(x + 50, 250, window=btn_correct)
    btns_correct.append(btn_correct)

    btn_wrong = tk.Button(root, text="✗", command=lambda i=i: check_answer(i, 0))
    btn_wrong.config(state=tk.NORMAL if i == current_question else tk.DISABLED)  # 只有当前问题的按钮是激活的
    canvas.create_window(x + 50, 300, window=btn_wrong)
    btns_wrong.append(btn_wrong)


  update_timer()

  

def end_game():
  if total_questions > 0:
    accuracy = total_correct / total_questions * 100
    result = f"你的正确率为：{accuracy:.2f}%,总共做了 {total_questions} 道题目。"
  else:
    result = "没有回答任何问题"
  result_label.config(text=result)
  for btn in btns_correct + btns_wrong:
      btn.config(state=tk.DISABLED)
  if accuracy<95:
    result = f"未达标     你的正确率为：{accuracy:.2f}%,总共做了 {total_questions} 道题目。"
  else:
    if total_questions<240:
      result = f"未达标     你的正确率为：{accuracy:.2f}%,总共做了 {total_questions} 道题目。"
    elif total_questions>480:
      result = "6"     
    else:
      result = "达标,但还得努力点"
    
  result_label.config(text=result)
  
 


root = tk.Tk()
root.title("808")

canvas = tk.Canvas(root, width=1400, height=400)
canvas.pack()

timer_label = tk.Label(root, text="剩余时间：300秒")
timer_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

btns_correct = []  # 存储正确按钮的列表
btns_wrong = []  # 存储错误按钮的列表

generate_triangles()

root.mainloop()


