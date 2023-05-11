variable "project_id" {
    default = "forecasting-test-382708"
}

variable "region" {
    default = "europe-west2"    
}

# for production deployments set this variable to false
variable "allow_data_deletion_on_tf_destroy" {
    default = true    
}