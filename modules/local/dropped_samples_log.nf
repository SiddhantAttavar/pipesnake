process DROPPED_SAMPLES_LOG {
    tag "Logging ${tuples.size()} dropped samples"

    input:
    val tuples

    output:
    path 'dropped_samples.csv'

    script:
    grouped = tuples.collate(2)

    """
    echo "sample_id,stage" > dropped_samples.csv
    ${ grouped.collect { "echo \"${it[0]},${it[1]}\" >> dropped_samples.csv" }.join('\n') }
    """
}
