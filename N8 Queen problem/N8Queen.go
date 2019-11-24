package main

import (
	"fmt"
	"time"
)

const (
	dim = 6
)

type board struct {
	cellOccu    [dim][dim]bool
	Queens      [dim]possition
	Prohibitios [dim][dim][dim]int // row,column,num of queen
	ProhibCheck [dim][dim]bool
}

type possition struct {
	row    int
	column int // column num=>a-h
}

var (
	p     = fmt.Println
	pf    = fmt.Printf
	step  int
	bo    board
	clmns = map[int]string{
		0:  "a",
		1:  "b",
		2:  "c",
		3:  "d",
		4:  "e",
		5:  "f",
		6:  "g",
		7:  "h",
		8:  "i",
		9:  "j",
		10: "k",
		11: "l",
		12: "m",
		13: "n",
		14: "o",
		15: "p",
	}
	pathCurr    [dim]possition
	paths       [4000][dim]possition
	pathNum     int
	cellToMove  []int
	solutions   [2700][dim]possition
	solutionNum int
)

func main() {
	start := time.Now()
	bo.walker(bo.FreePlaces(0))

	p("Paths walked:", pathNum)
	p("Solutions found:", solutionNum)
	dur := time.Now().Sub(start)
	p(dur.Seconds(), "seconds")
}

func (bo *board) addQueen(row int) {
	bo.cellOccu[row][step] = true
	bo.Queens[step].row = row
	bo.Queens[step].column = step
	pathCurr[step].row = row
	pathCurr[step].column = step

	// optimization
	// cells under attack
	for i := step; i < dim; i++ {
		bo.ProhibCheck[row][i] = true
	}
	for r, c := 1, 1; row+r < dim && step+c < dim; r, c = r+1, c+1 {
		bo.ProhibCheck[row+r][step+c] = true
	}
	for r, c := -1, 1; row+r >= 0 && step+c < dim; r, c = r-1, c+1 {
		bo.ProhibCheck[row+r][step+c] = true
	}
	// --optimization
}

func (bo *board) printPrCheck() {
	for r := dim - 1; r >= 0; r-- {
		pf("%d ", r+1)
		if r < 9 {
			pf(" ")
		}
		for c := 0; c < dim; c++ {
			if bo.cellOccu[r][c] {
				pf("[Q]")
			} else if bo.ProhibCheck[r][c] || c < step {
				pf("[-]")
			} else {
				pf("[ ]")
			}
		}
		pf("\n")
	}
	pf("    a  b")
	if dim > 2 {
		for i := 2; i < dim; i++ {
			pf("  %s", clmns[i])
		}
	}
	pf("\n")
}

func (bo *board) FreePlaces(col int) []int {
	free := make([]int, 0, dim)
	for i := 0; i < dim; i++ {
		if !bo.ProhibCheck[i][col] {
			free = append(free, i)
		}
	}
	return free
}

func (bo *board) remQueen() {
	bo.cellOccu[bo.Queens[step].row][bo.Queens[step].column] = false
	pathCurr[step].row = 0
	pathCurr[step].column = 0

	// optimization
	// nullizer
	for r := 0; r < dim; r++ {
		for c := 0; c < dim; c++ {
			bo.ProhibCheck[r][c] = false
		}
	}
	for i := 0; i < step; i++ {
		rQ := bo.Queens[i].row
		cQ := bo.Queens[i].column
		for j := i; j < dim; j++ {
			bo.ProhibCheck[rQ][j] = true
		}
		for r, c := 1, 1; rQ+r < dim && cQ+c < dim; r, c = r+1, c+1 {
			bo.ProhibCheck[rQ+r][cQ+c] = true
		}
		for r, c := -1, 1; rQ+r >= 0 && cQ+c < dim; r, c = r-1, c+1 {
			bo.ProhibCheck[rQ+r][cQ+c] = true
		}
	}
	// --optimization
}

func (bo *board) walker(freeCells []int) {
	for _, r := range freeCells {
		bo.addQueen(r)

		// Last queen on table
		if step == dim-1 {
			if solutionNum%10000 == 0 {
				p("Path found! step:", pathNum+1, "solution:", solutionNum+1)
			}
			for i := 0; i < dim; i++ {
				pf("{%s%d}", clmns[pathCurr[i].column], pathCurr[i].row+1)
			}
			pf("\n")
			bo.printPrCheck()
			if dim < 10 {
				paths[pathNum] = pathCurr
			}
			pathNum++
			if dim < 12 {
				solutions[solutionNum] = pathCurr
			}
			solutionNum++
			bo.remQueen()
			continue
		}

		// Checking places to put queen
		nextFCells := bo.FreePlaces(step + 1)
		if len(nextFCells) == 0 {
			if dim < 10 {
				pf("%d Stuck on step: %d path: ", pathNum+1, step+1)
				for i := 0; i <= step; i++ {
					pf("{%s%d}", clmns[pathCurr[i].column], pathCurr[i].row+1)
				}
				pf("\n")

				paths[pathNum] = pathCurr
			}
			pathNum++
			bo.remQueen()
			continue
		}
		step++
		bo.walker(nextFCells)

		bo.remQueen()
	}

	// step back
	step--
}

// no need more
func (bo *board) calcProhib() {
	// nullizer
	for r := 0; r < dim; r++ {
		for c := 0; c < dim; c++ {
			bo.ProhibCheck[r][c] = false
			for i := 0; i < dim; i++ {
				bo.Prohibitios[r][c][i] = 0
			}
		}
	}

	// num queen
	for i := 0; i <= step; i++ {
		rQ := bo.Queens[i].row
		cQ := bo.Queens[i].column
		// p("rQ", rQ, " cQ", cQ)
		// rows
		for r := 0; r < dim; r++ {
			// give num of queen
			bo.Prohibitios[r][cQ][i] = i + 1
		}
		// columns
		for c := 0; c < dim; c++ {
			bo.Prohibitios[rQ][c][i] = i + 1
		}
		// diagonal
		for r, c := 1, 1; rQ+r < dim && cQ+c < dim; r, c = r+1, c+1 {
			bo.Prohibitios[rQ+r][cQ+c][i] = i + 1
		}
		for r, c := -1, 1; rQ+r >= 0 && cQ+c < dim; r, c = r-1, c+1 {
			bo.Prohibitios[rQ+r][cQ+c][i] = i + 1
		}
		for r, c := 1, -1; rQ+r < dim && cQ+c >= 0; r, c = r+1, c-1 {
			bo.Prohibitios[rQ+r][cQ+c][i] = i + 1
		}
		for r, c := -1, -1; rQ+r >= 0 && cQ+c >= 0; r, c = r-1, c-1 {
			bo.Prohibitios[rQ+r][cQ+c][i] = i + 1
		}
	}

	// cells under attack
	for r := 0; r < dim; r++ {
		for c := 0; c < dim; c++ {
			for i := 0; i <= step; i++ {
				if bo.Prohibitios[r][c][i] != 0 {
					bo.ProhibCheck[r][c] = true
					break
				}
			}
		}
	}
}

// no need more
func (bo *board) printProh() {
	var cellS string
	for r := dim - 1; r >= 0; r-- {
		pf("\n")
		pf("%d ", r+1)
		for rows := 1; rows <= 2; rows++ {
			if rows == 2 {
				pf("  ")
			}
			for c := 0; c < dim; c++ {
				for i := 4*rows - 4; i <= 4*rows-1; i++ {
					if bo.Prohibitios[r][c][i] != 0 {
						cellS += fmt.Sprintf("%d,", bo.Prohibitios[r][c][i])
					} else {
						cellS += "  "
					}
				}
				pf("[%s]", cellS)
				cellS = ""
			}
			pf("\n")
		}
		// pf("\n")
	}
	p("      a)        b)        c)        d)        e)        f)        g)        h)\n")
}

/*`
n	fundamental	all
1	1	1
2	0	0
3	0	0
4	1	2
5	2	10
6	1	4
7	6	40
8	12	92
9	46	352
10	92	724
11	341	2,680
12	1,787	14,200
13	9,233	73,712
14	45,752	365,596
15	285,053	2,279,184
16	1,846,955	14,772,512
17	11,977,939	95,815,104
18	83,263,591	666,090,624
19	621,012,754	4,968,057,848
20	4,878,666,808	39,029,188,884
21	39,333,324,973	314,666,222,712
22	336,376,244,042	2,691,008,701,644
23	3,029,242,658,210	24,233,937,684,440
24	28,439,272,956,934	227,514,171,973,736
25	275,986,683,743,434	2,207,893,435,808,352
26	2,789,712,466,510,289	22,317,699,616,364,044
27	29,363,495,934,315,694	234,907,967,154,122,528
`
*/
