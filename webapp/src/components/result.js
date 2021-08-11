import { Result } from "@elastic/react-search-ui";

<SearchProvider config={config}>
  {({ results }) => {
    return (
      <div>
        {results.map(result => (
          <Result key={result.id.raw}
            result={result}
            titleField="title"
            urlField="nps_link"
          />
        ))}
      </div>
    );
  }}
</SearchProvider>