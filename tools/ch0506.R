suppressPackageStartupMessages({library(psych); library(effectsize)})

cat("===== 5장: 제1종 오류 누적 =====\n")
for (k in 2:6) {
  c_ <- choose(k, 2)
  cat(sprintf("집단 %d개 | 비교 %2d회 | 최소 1회 오류 확률 %.4f\n", k, c_, 1 - .95^c_))
}

cat("\n===== 5장: 표본크기만 키웠을 때 =====\n")
# 원고 예: 100점 만점, mu=30, 처치 후 M=31, SD=15
for (n in c(50, 100, 400, 1000)) {
  z <- (31 - 30) / (15 / sqrt(n))
  cat(sprintf("n=%4d | SE=%.3f | z=%.3f | p=%.4f | d=%.3f\n",
      n, 15/sqrt(n), z, 2*pnorm(-abs(z)), (31-30)/15))
}

cat("\n===== 5장: 검정력 =====\n")
for (n in c(20, 30, 50, 64, 100)) {
  p <- power.t.test(n = n, delta = 0.5, sd = 1, sig.level = .05)$power
  cat(sprintf("각 집단 n=%3d | d=0.50 | 검정력 = %.3f\n", n, p))
}
cat("\n검정력 .80을 맞추려면:\n")
print(power.t.test(delta = 0.5, sd = 1, sig.level = .05, power = .80))

cat("\n유의수준을 바꾸면 (각 집단 n=30, d=0.5):\n")
for (a in c(.01, .05, .10)) {
  cat(sprintf("alpha=%.2f | 검정력 = %.3f\n", a,
      power.t.test(n = 30, delta = .5, sd = 1, sig.level = a)$power))
}

cat("\n===== 6장: 신뢰구간 시뮬레이션 =====\n")
set.seed(2025)
mu <- 3.5; sigma <- 0.83; n <- 30
hit <- 0; res <- NULL
for (i in 1:100) {
  x  <- rnorm(n, mu, sigma)
  ci <- mean(x) + c(-1, 1) * qt(.975, n - 1) * sd(x) / sqrt(n)
  ok <- ci[1] <= mu && mu <= ci[2]
  hit <- hit + ok
  res <- rbind(res, c(m = mean(x), lo = ci[1], hi = ci[2], ok = ok))
}
cat(sprintf("100개 표본 중 모평균 %.2f를 포함한 신뢰구간: %d개\n", mu, hit))
write.csv(round(as.data.frame(res), 4), "tools/ci_sim.csv", row.names = FALSE)

cat("\n===== 6장: 단일표본 t-검정 =====\n")
df <- read.csv("books/01-basic-statistics/data/sample_data.csv")
s <- df$selfesteem
cat(sprintf("n=%d M=%.3f SD=%.3f SE=%.4f\n", length(s), mean(s), sd(s), sd(s)/sqrt(length(s))))
print(t.test(s, mu = 3.0))
cat("\n-- 기준값을 3.4로 바꾸면 --\n")
print(t.test(s, mu = 3.4)$p.value)

cat("\n===== 6장: t분포와 z분포의 임계값 =====\n")
for (dfree in c(5, 10, 30, 60, 120, 1000)) {
  cat(sprintf("df=%5d | t 임계값 = %.3f\n", dfree, qt(.975, dfree)))
}
cat(sprintf("z 임계값 = %.3f\n", qnorm(.975)))

cat("\n===== 6장: 표본크기별 신뢰구간 폭 =====\n")
for (nn in c(25, 100, 240, 400)) {
  half <- qt(.975, nn - 1) * sd(s) / sqrt(nn)
  cat(sprintf("n=%3d | 반폭 = %.4f | 구간 폭 = %.4f\n", nn, half, 2*half))
}
