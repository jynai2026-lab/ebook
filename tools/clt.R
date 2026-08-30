set.seed(2025)
pop <- rexp(200000, rate = 1)
out <- list()
grab <- function(v, from, to) {
  d <- density(v, from = from, to = to, n = 90)
  list(x = d$x, y = d$y, sd = sd(v), skew = psych::skew(v))
}
suppressPackageStartupMessages(library(psych))
res <- list(pop = grab(pop, 0, 5))
for (n in c(5, 30)) {
  res[[paste0("n", n)]] <- grab(replicate(5000, mean(sample(pop, n))), 0, 3)
}
cat("{\n")
ks <- names(res)
for (i in seq_along(ks)) {
  o <- res[[ks[i]]]
  cat(sprintf('"%s":{"x":[%s],"y":[%s],"sd":%.4f,"skew":%.3f}%s\n', ks[i],
      paste(round(o$x,4), collapse=","), paste(round(o$y,5), collapse=","),
      o$sd, o$skew, if (i < length(ks)) "," else ""))
}
cat("}\n")
