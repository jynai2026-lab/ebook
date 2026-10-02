# 그림용 자료를 만든다. 그림은 tools/fig2_*.py 가 이 JSON을 읽어 그린다.
#
#   Rscript books/02-regression/r/figdata.R
#
# 책에 실린 숫자와 그림이 같은 자료에서 나오도록, 그림의 점·선도 R이 계산한다.
suppressPackageStartupMessages(library(jsonlite))
setwd(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))), ".."))
d <- read.csv("data/survey.csv")
d$position <- factor(d$position, levels = c("사원", "대리", "과장이상"))
out <- function(x, name) write_json(x, file.path("figdata", name), digits = 6, auto_unbox = TRUE)

# ---- 1장
out(list(x = d$stress, y = d$burnout, mx = mean(d$stress), my = mean(d$burnout),
         r = cor(d$stress, d$burnout)), "ch01-stress-burnout.json")
out(lapply(1:4, function(i) list(x = anscombe[[i]], y = anscombe[[i + 4]],
                                 r = cor(anscombe[[i]], anscombe[[i + 4]]))), "ch01-anscombe.json")
out(list(x = d$tenure, y = d$satisfaction, g = as.character(d$position),
         r = cor(d$tenure, d$satisfaction),
         within = sapply(split(d, d$position), function(g) cor(g$tenure, g$satisfaction)),
         gmx = tapply(d$tenure, d$position, mean), gmy = tapply(d$satisfaction, d$position, mean)),
    "ch01-third.json")

# ---- 2장
fit <- lm(burnout ~ stress, d)
grid <- seq(1.2, 4.6, by = .05)
ci <- predict(fit, data.frame(stress = grid), interval = "confidence")
pi <- predict(fit, data.frame(stress = grid), interval = "prediction")
out(list(x = d$stress, y = d$burnout, b0 = coef(fit)[[1]], b1 = coef(fit)[[2]],
         fitted = unname(fitted(fit)), grid = grid,
         ci_lo = ci[, "lwr"], ci_hi = ci[, "upr"], pi_lo = pi[, "lwr"], pi_hi = pi[, "upr"]),
    "ch02-fit.json")
cat("figdata 완료\n")

# ---- 4장
fit3 <- lm(burnout ~ stress + support + efficacy, d)
qq <- qqnorm(rstandard(fit3), plot.it = FALSE)
out(list(fitted = unname(fitted(fit3)), resid = unname(resid(fit3)),
         qx = unname(qq$x), qy = unname(qq$y),
         cook = unname(cooks.distance(fit3)), hat = unname(hatvalues(fit3))), "ch04-diag.json")
set.seed(1)
arousal <- runif(200, 1, 5)
perf <- 1 + 2.88 * arousal - 0.48 * arousal^2 + rnorm(200, 0, .5)
m_line <- lm(perf ~ arousal); m_curve <- lm(perf ~ arousal + I(arousal^2))
out(list(x = arousal, y = perf, line = unname(coef(m_line)), curve = unname(coef(m_curve))), "ch04-curve.json")
cat("figdata 4장 완료\n")

# ---- 5장
m_both <- lm(burnout ~ stress + workload + support, d)
m_s <- lm(burnout ~ stress + support, d); m_w <- lm(burnout ~ workload + support, d)
ci <- function(m, v) unname(c(coef(m)[v], confint(m)[v, ]))
set.seed(1); i <- sample(nrow(d), 150); A <- d[i, ]; B <- d[-i, ]
fb <- burnout ~ stress + workload + support; fo <- burnout ~ stress + support
out(list(stress_alone = ci(m_s, "stress"), stress_both = ci(m_both, "stress"),
         load_alone = ci(m_w, "workload"), load_both = ci(m_both, "workload"),
         split_both = list(A = unname(coef(lm(fb, A))[2:3]), B = unname(coef(lm(fb, B))[2:3])),
         split_one = list(A = unname(coef(lm(fo, A))[2]), B = unname(coef(lm(fo, B))[2]))),
    "ch05.json")
cat("figdata 5장 완료\n")

# ---- 8장
d$stress_c <- d$stress - mean(d$stress); d$support_c <- d$support - mean(d$support)
m_int <- lm(burnout ~ efficacy + stress_c * support_c, d)
b <- coef(m_int); V <- vcov(m_int); s <- sd(d$support)
ws <- seq(min(d$support), max(d$support), by = .01) - mean(d$support)
sl <- b["stress_c"] + b["stress_c:support_c"] * ws
se <- sqrt(V["stress_c", "stress_c"] + ws^2 * V["stress_c:support_c", "stress_c:support_c"] +
           2 * ws * V["stress_c", "stress_c:support_c"])
crit <- qt(.975, df.residual(m_int))
out(list(b = unname(b), mx = mean(d$stress), mw = mean(d$support), sw = s, me = mean(d$efficacy),
         x = d$stress, y = d$burnout, w = d$support,
         jn_w = ws + mean(d$support), jn_sl = unname(sl), jn_lo = unname(sl - crit * se), jn_hi = unname(sl + crit * se)),
    "ch08.json")
cat("figdata 8장 완료\n")

# ---- 9장 (부트스트랩 2,000회: 원고와 같은 시드)
suppressPackageStartupMessages(library(lavaan))
model9 <- '
  burnout  ~ a * stress
  turnover ~ b * burnout + cp * stress
  indirect := a * b
  total    := cp + a * b
'
set.seed(2026)
fit9 <- sem(model9, data = d, se = "bootstrap", bootstrap = 2000)
pe9 <- parameterEstimates(fit9, boot.ci.type = "perc")
bt9 <- lavInspect(fit9, "boot")
out(list(ab = unname(bt9[, "a"] * bt9[, "b"]),
         est = pe9$est[pe9$label == "indirect"],
         lo = pe9$ci.lower[pe9$label == "indirect"], hi = pe9$ci.upper[pe9$label == "indirect"]),
    "ch09-boot.json")
cat("figdata 9장 완료\n")
