# Function to display files and allow user selection
select_file <- function(directory='../Output',display=T,return_data=T) {
  # Get the list of files in the specified directory
  files <- list.files(directory,pattern = "_")#To ensure it's one of my saves
  
  # Check if there are any files
  if (length(files) == 0) {
    cat("No files found in the directory.\n")
    return(NULL)
  }
  
  # Display the list of files
  cat("Files available in the directory:\n")
  for (i in seq_along(files)) {
    cat(i, ": ", files[i], "\n", sep = "")
  }
  
  # Prompt user for selection
  repeat {
    cat("Please enter the number of the file you want to display (1-", length(files), "): ", sep = "")
    selection <- as.integer(readline())
    
    # Check if the selection is valid
    if (!is.na(selection) && selection >= 1 && selection <= length(files)) {
      selected_file <- files[selection]
      cat("You selected: ", selected_file, "\n", sep = "")
      break
    } else {
      cat("Invalid selection. Please try again.\n")
    }
  }
  
  tab = read.csv(paste0(directory,'\\',selected_file), header=TRUE)
  if (display){
    View(tab)
  }
  if (return_data){
    return(tab)  
  }
}

select_log <- function(directory='../Output/Logs',display=T,return_data=T) {
  # Get the list of files in the specified directory
  files <- list.files(directory,pattern = "_")#To ensure it's one of my saves
  
  # Check if there are any files
  if (length(files) == 0) {
    cat("No files found in the directory.\n")
    return(NULL)
  }
  
  # Display the list of files
  cat("Files available in the directory:\n")
  for (i in seq_along(files)) {
    cat(i, ": ", files[i], "\n", sep = "")
  }
  
  # Prompt user for selection
  repeat {
    cat("Please enter the number of the file you want to display (1-", length(files), "): ", sep = "")
    selection <- as.integer(readline())
    
    # Check if the selection is valid
    if (!is.na(selection) && selection >= 1 && selection <= length(files)) {
      selected_file <- files[selection]
      cat("You selected: ", selected_file, "\n", sep = "")
      break
    } else {
      cat("Invalid selection. Please try again.\n")
    }
  }
  
  tab = read.csv(paste0(directory,'\\',selected_file), header=F, sep='\t')
  if (display){
    View(tab)
  }
  if (return_data){
    return(tab)  
  }
}

select_file(return_data=F)

select_log(return_data=F)


# Accuracys
tab = select_file(display=F)

mean(tab$Gabor_Acc)

tab$Updated_belief
tab$Belief_alone
tab$Sampled
