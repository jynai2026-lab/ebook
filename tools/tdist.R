# 4장 그림용 t분포 값 — 실제 검정 결과와 같은 자유도로 계산
df <- 238
x  <- seq(-4.5, 4.5, length.out = 160)
y  <- dt(x, df)
crit <- qt(0.975, df)          # 양측 .05 임계값
obs  <- -3.9343                # 본문의 검정통계량

cat("{\n")
cat(sprintf('"x":[%s],\n', paste(round(x,4), collapse=",")))
cat(sprintf('"y":[%s],\n', paste(round(y,6), collapse=",")))
cat(sprintf('"df":%d,"crit":%.4f,"obs":%.4f,\n', df, crit, obs))
cat(sprintf('"p":%.6f\n', 2*pt(obs, df)))
cat("}\n")

# 표본크기가 p값에 미치는 영향 — 같은 평균차·표준편차에서 n만 바꾼다
cat("\n--- 표본크기별 p값 (평균차 0.15, SD 0.8 고정) ---\n", file = stderr())
for (n in c(20, 50, 100, 300, 1000)) {
  se <- 0.8 * sqrt(2/n); t <- 0.15/se; p <- 2*pt(-abs(t), 2*n-2)
  cat(sprintf("n=%4d  t=%5.2f  p=%.4f\n", n, t, p), file = stderr())
}
