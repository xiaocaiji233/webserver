window.onload = () => {
    const json = document.getElementById('json')
    const item = JSON.parse(json.textContent)
    console.log(item)
    const data = []
    Object.keys(item).map(i => {
        data.push({
            label: i,
            type: 'stars',
            value: item[i].stargazers_count,
        })
        data.push({
            label: i,
            type: 'forks',
            value: item[i].forks_count,
        })
        data.push({
            label: i,
            type: 'watchers',
            value: item[i].watchers_count,
        })
    })

  var chart = new G2.Chart({
    container: 'mountNode',
    forceFit: true,
    height: window.innerHeight
  });
  chart.source(data);
  chart.axis('value', {
    position: 'top'
  });
  chart.axis('label', {
    label: {
      offset: 12
    }
  });
  // chart.coord().transpose().scale(1, -1);
  chart.interval().position('label*value').color('type').adjust([{
        type: 'dodge',
        marginRatio: 1 / 32
    }]);
  chart.render();
}