# Set seed
set.seed(123)

# Set global 
sample_size <- 1000
intercept <- 4.0
b1 <- -0.2
b2 <- -0.3
b3 <- 0.1
n_reps <- 1:10000

# Make empty data frame for simulation results
result_sim = data.frame(matrix(vector(), 0, 6,
                       dimnames=list(c(), c("F full", 
                                            "F df full", 
                                            "F p full", 
                                            "F rank def",
                                            "F df rank def",
                                            "F p rank def"))))

# Simulate n regressions and store results related to the F-tests
for (i in n_reps){
  cat('Calculating iteration #:', str(i), 'out of ', str(max(n_reps)), '\n')
  x1 <- sample(rep(c(1, 2, 3), sample_size), sample_size) # Simulate a vector, "sample" randomizes the ordering
  x2 <- sample(rep(c(1, 2, 3, 4), sample_size), sample_size)
  y <- intercept + b1 * x1 + b2 * x2 + b3 *x1*x2 + rnorm(sample_size)
  df <- data.frame(x1, x2, y)
  
  #Full model
  # Only main effects
  reg0 <- lm(y ~ factor(x1) + factor(x2), data = df)
  # With interaction
  reg1 <- lm(y ~ factor(x1) + factor(x2) + factor(x1):factor(x2), data = df)
  # F test
  ftest_full <- anova(reg0, reg1)
  result_sim[i, "F.df.full"] <- ftest_full$Df[2]
  result_sim[i, "F.full"] <- ftest_full$F[2]
  result_sim[i, "F.p.full"] <- ftest_full$`Pr(>F)`[2]
  
  #Rank deficient model
  
  df2 <- filter(df, ! ((x1 == 1) & (x2 == 2)))
  df2 <- filter(df2, ! ((x1 == 2) & (x2 == 3)))
  df2 <- filter(df2, ! ((x1 == 3) & (x2 == 1)))
  df2 <- filter(df2, ! ((x1 == 2) & (x2 == 1)))
  
  #Without interaction
  reg0_def <- lm(y ~ factor(x1) + factor(x2), data = df2)
  # With interaction
  reg1_def <- lm(y ~ factor(x1) + factor(x2) + factor(x1):factor(x2), data = df2)
  summary <- summary(reg1_def)
  # F test
  ftest_def <- anova(reg0_def, reg1_def)
  result_sim[i, "F.rank.def"] <- ftest_def$Df[2]
  result_sim[i, "F.df.rank.def"] <- ftest_def$F[2]
  result_sim[i, "F.p.rank.def"] <- ftest_def$`Pr(>F)`[2]
  
}

#Proportion of p-values below 0.05 
p_vals_full <- nrow(result_sim[result_sim$F.p.full < 0.05, ]) / nrow(result_sim) * 100
p_vals_def  <- nrow(result_sim[result_sim$F.p.rank.def < 0.05, ]) / nrow(result_sim) * 100

#Create histograms for full and rank deficient regressions
p_full <- gghistogram(
  result_sim, x = "F.p.full", bins=100, ylab = "Count", xlab = "p-values") +
  geom_vline(xintercept = 0.05, colour="red", linetype = "longdash") + 
  ggtitle('Not rank-deficient model')

p_def <- gghistogram(
  result_sim, x = "F.p.rank.def", bins=100, ylab = "Count", xlab = "p-values") +
  geom_vline(xintercept = 0.05, colour="red", linetype = "longdash") + 
  ggtitle('Rank-deficient model')


# Make into one plot
ggarrange(p_full, p_def, 
          labels = c('A', 'B'), 
          ncol = 2, 
          nrow = 1)





