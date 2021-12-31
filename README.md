# Optimization-Project
A solution for multiple (minimax) asymmetric travelling salesman problem (m-ATSP)

Problem: Allocate work to workers

• There are N customers 1, 2, …, N need to maintain the internet network. Customer i is at location i (i = 1,…,N)

• Maintenance for customer i lasts d(i) time unit(s)

• There are K technical staffs at the company's headquarters (point 0) and has a starting time of t0 = 0.

• Travel time from point i to point j takes t(i,j)

• Plan to assign maintenance staff to customers so that the maximum working time (travel time plus maintenance time) of a certain employee is minimal.


Code and idea based mostly from the paper "Tournament Selection Algorithm for the Multiple Travelling Salesman Problem" of Giorgos Polychronis & Spyros Lalis with some adjustments and comments.
Refer link: "https://www.scitepress.org/Papers/2020/95649/95649.pdf"

#comment
Overall, this is a really nice algorithm, with just tournament selection, it already found better solution than any others algorithms in our class.
With large neighborhood search, even though after changing mutation coefficient many times, it still could't find better solution for which gains from tournament selection, every genres created by mutations are always worse than that of initial solution.
So I conclude that each solution from TS is already a best gen of itself.
