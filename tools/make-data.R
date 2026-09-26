set.seed(20250725)

# 종속표본용: 사전-사후 (8장)
n <- 40
pre  <- round(pmin(pmax(rnorm(n, 3.10, 0.70), 1), 5), 2)
post <- round(pmin(pmax(pre + rnorm(n, 0.38, 0.55), 1), 5), 2)
write.csv(data.frame(id = 1:n, pre = pre, post = post),
          "books/01-basic-statistics/data/prepost.csv", row.names = FALSE)

# 일원분산분석용: 원고의 교수법 예제 (9~10장)
teach <- data.frame(
  method = factor(rep(c("A","B","C"), each = 10)),
  score  = c(65,70,68,70,62,70,74,68,70,65,
             69,73,74,75,67,77,78,75,73,75,
             75,74,77,80,70,81,79,78,79,80))
write.csv(teach, "books/01-basic-statistics/data/teaching.csv", row.names = FALSE)

cat("prepost.csv, teaching.csv 생성\n")
