suppressPackageStartupMessages(library(car))
tw <- read.csv("books/01-basic-statistics/data/twoway.csv")
tw$gender <- factor(tw$gender); tw$school <- factor(tw$school)

cat("===== 셀 평균 =====\n")
print(round(tapply(tw$score, list(tw$gender, tw$school), mean), 2))
cat("\n주변평균 (성별):\n"); print(round(tapply(tw$score, tw$gender, mean), 2))
cat("주변평균 (학교):\n");  print(round(tapply(tw$score, tw$school, mean), 2))

cat("\n===== Levene =====\n")
print(leveneTest(score ~ gender * school, data = tw))

cat("\n===== 이원분산분석 (제3유형) =====\n")
options(contrasts = c("contr.sum", "contr.poly"))
m <- aov(score ~ gender * school, data = tw)
print(Anova(m, type = 3))

cat("\n===== 기본(제1유형) =====\n")
print(summary(aov(score ~ gender * school, data = tw)))

cat("\n===== 셀별 n, 평균, 표준편차 =====\n")
agg <- aggregate(score ~ gender + school, data = tw,
                 FUN = function(x) c(n = length(x), M = mean(x), SD = sd(x)))
print(do.call(data.frame, agg), digits = 4)

cat("\n===== 단순주효과: 성별별로 학교 효과 =====\n")
for (g in levels(tw$gender)) {
  sub <- subset(tw, gender == g)
  cat("\n[", g, "]\n"); print(summary(aov(score ~ school, data = sub)))
}

cat("\n===== 효과크기 (부분 eta 제곱) =====\n")
suppressPackageStartupMessages(library(effectsize))
print(eta_squared(Anova(m, type = 3), partial = TRUE))
