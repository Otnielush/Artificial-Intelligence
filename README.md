# Artificial-Intelligence
Different algorithms for analysis and decision making

# 4 in a Row
   The algorithm calculates the usefulness of only one move per turn. Calculates before its turn and before the player’s turn. Before the player’s turn, in order to understand whether the player aggressively made a move. Did he choose a less profitable option for himself in order to prevent his opponent. If the move is aggressive, then AI also attacks the player to the detriment of himself. Now all estimates of the turn gain for the opponent are multiplied by 2 and the AI ​​chooses to attack the player.
#### Each one must be weighed for the following cases: 
* victory (4 in a row), 
* 3 in a row, 2 in a row, 
* 1 in a row 
* for free cells in a row.  

When a series of no more than 3 cells (closed by an opponent), only empty cells and individual symbols are evaluated, but not as a combination.  

 Evaluation is done both for the benefit of the AI and the opponent, and then they add up. The cell with the highest score wins. In non-aggressive mode, the score for the opponent’s moves is 85% so that the AI ​​would prefer to develop rather than push. The combination is calculated in a row, in a column and diagonally.
#### Weights are selected approximately and then edited on checks: 
* 400 for 4 in a row, 
* 100 for 3 in a row, 
* 35 for 2 in a row 
* for individual characters. 

There is also a coefficient for height. If the cell is located above the other cells, then its weight decreases. But still, the AI ​​will choose to build a combination instead of a single character.  
 
#### 3 strategies for responding to an opponent’s aggression: 
* 1 attack move, 
* attack endlessly 
* 3 attacks and then standard mode. 

But since the game often has to interfere with the opponent, the 2nd and 3rd modes are the same.  
  
  In the code, the weights for AI are loaded from the file or used by default. This was done in order to do self-training for AI, so that it regulates weights on the basis of wins / losses, but it was never realized.  
  
  You can defeat AI if you calculate the winning move 2 forward.
  
---
  Алгоритм расчитывает на каждом ходу полезность только одного хода. Расчитывает перед своим ходом и перед ходом игрока. Перед ходом игрока для того чтобы понять агрессивно ли сделал ход игрок. Выбрал ли он менее выгодня для себя вариант хода для того чтобы напредить сопернику. Если ход агресивный, то AI тоже атакует игрока в ущерб себе. Теперь все оценки выгоды хода для соперника умножаются на 2 и AI выбирает атаковать игрока.  
#### Оценка каждого производиться весами для случаев: 
* победа(4 в ряд), 
* 3 в ряд, 2 в ряду, 
* 1 в ряду 
* за свободные клетки в ряду. 

Когда ряд не более 3 клеток(закрыт соперником) то оцениваются только пустые клетки и отдельные свои символы, но не как комбинация.  
  
Оценка делается как выгода для AI так и для соперника, а потом складываются. Клетка получившая наибольшую оценку побеждает. В не агрессивном режиме оценка для ходов соперника стоит на 85% чтобы AI предпочитал развиваться,а не наподать. Расчёт комбинаций происходит в ряд, в столб и по диагоналям. 
#### Веса подобранны приблизительно и потом на проверках подредактированы: 
* 400 для 4 в ряд, 
* 100 для 3 в ряд, 
* 35 для 2 в ряд 
* для отдельных символов. 

Так же есть коэфициент для высоты. Если ячейка расположена выше остальных ячеек то её вес уменьшается. Но всё равно AI выберет построить комбинацию вместо одиночного символа.  

#### 3 стратегии для реакции на агрессию соперника: 
* 1 ход атаки, 
* бесконечно атаковать 
* 3 атаки и потом стандартный режим. 

Но так как в игре часто приходиться мешать сопернику то 2-й и 3-й режим одинаковы.  
  
  В коде веса для AI загружаются из файла или же используются поумолчанию. Это было сделано для того чтобы сделать самообучения для AI, чтобы он регулировал веса на основе побед/проигрышей, но так и небыло реализовано.  
  
  Можно победить AI если расчитать победный ход на 2 вперёд.
